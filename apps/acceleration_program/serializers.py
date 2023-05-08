from typing import OrderedDict

from django.core.exceptions import NON_FIELD_ERRORS
from rest_framework import serializers

from apps.acceleration_program.models import (
    AccelerationProgram,
    JoinProgram,
    Applicants,
    Stage,
    ApplicantResponse,
    StuffResponseDescription,
)
from apps.accounts.models import CustomUserModel


class AccelerationProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccelerationProgram
        fields = [
            "id",
            "name",
            "requirements",
            "directions",
            "program_start_time",
            "program_end_time",
            "registration_start_date",
            "registration_end_date",
            "is_active",
        ]

    def validate(self, attrs: "OrderedDict") -> "OrderedDict":
        """
        Method that validates AccelerationProgram instance based on name and status
        E.g:
            name = Foo
            status = True
            And data in DB is already with this name and status, it will raise exception
        """
        name, status = attrs.get("name"), attrs.get("is_active")
        if AccelerationProgram.objects.filter(name=name, is_active=True):
            raise serializers.ValidationError({"detail": "Active acceleration program with this name already exists"})
        return attrs

    @staticmethod
    def create_joinprogram_template(instance: "AccelerationProgram") -> None:  # noqa
        """
        After calling this method templates of JoinProgram should be created based on chosen direction
        """

        for direction in instance.directions.all():
            JoinProgram.objects.update_or_create(program_id=instance.id, direction=direction)


class JoinProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinProgram
        fields = "__all__"


class RegisteredApplicantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicants
        fields = "__all__"


class ApplicantsRegistrationSerializer(serializers.ModelSerializer):
    applicant = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Applicants
        fields = ["id", "applicant", "program_to_join"]

    def create(self, validated_data):
        applicant = Applicants(
            program_to_join=validated_data["program_to_join"], applicant=self.context["request"].user
        )
        applicant.save()
        return applicant


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ["id"]


class ApplicantResponseSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ApplicantResponse
        fields = ["id", "applicant", "stage", "direction", "applicant_response_description"]

    def validate(self, attrs: "OrderedDict") -> "OrderedDict":
        """TODO doc"""
        user_id = self.context.get("request").user.id
        stage = attrs.get("stage")
        direction = attrs.get("direction")

        applicant = Applicants.objects.filter(applicant_id=user_id)

        if not applicant:
            raise serializers.ValidationError({"detail": "You are not registered as applicant."})

        if not stage.joinprogram_set.first():
            raise serializers.ValidationError(
                {"detail": "You can't send response. Maybe stage exists but for program it isn't registered yet."}
            )

        if applicant.filter(request_status="Pending"):
            raise serializers.ValidationError(
                {
                    "detail": "Your request to join as an applicant is pending. "
                    "Please wait or contact to our site administration"
                }
            )

        elif applicant.filter(request_status="Rejected"):
            raise serializers.ValidationError(
                {"detail": "Your request to join as an applicant is rejected so you can't send response."}
            )

        if not applicant.filter(program_to_join__direction=direction):
            raise serializers.ValidationError(
                {"detail": "Your response direction isn't appropriate for this stage, please fix it."}
            )

        if Stage.objects.filter(applicantresponse__applicant=user_id, applicantresponse__status="Rejected"):
            raise serializers.ValidationError(
                {"detail": "You are rejected in previous stage, therefore you can't send response."}
            )

        return attrs


class StuffResponseDescriptionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = StuffResponseDescription
        fields = ["id", "author", "applicant_response", "description", "status"]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("author", "applicant_response"),
                message="You have already evaluated this applicant_response. "
                "You can't create a new one, maybe you can use your previous response to update.",
            )
        ]

    def validate(self, attrs: "OrderedDict") -> "OrderedDict":
        """In this method applicant_response status will change based on stuff evaluation"""

        applicant_response: "ApplicantResponse" = attrs["applicant_response"]
        status = attrs["status"]  # STATUS THAT DETERMINES IF APPLICANT RESPONSE IS ACCEPTED OR REJECTED
        applicant_response.status = status
        applicant_response.save()

        return attrs
