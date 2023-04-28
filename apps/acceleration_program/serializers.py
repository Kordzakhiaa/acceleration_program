from typing import OrderedDict

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

    def validate(self, attrs):
        user_id = self.context.get("request").user.id
        stage = attrs.get("stage")
        direction = attrs.get("direction")

        applicant = Applicants.objects.filter(applicant_id=user_id)

        if not applicant:
            raise serializers.ValidationError({"detail": "You are not registered as applicant."})

        if not stage.joinprogram_set.first():
            raise serializers.ValidationError({"detail": "You can't send response because there is no stage(s) yet."})

        if applicant.filter(request_status="Pending"):
            raise serializers.ValidationError(
                {"detail": "Your request status is pending. Please wait or contact to our site administration"}
            )

        elif applicant.filter(request_status="Rejected"):
            raise serializers.ValidationError({"detail": "Your request status is rejected so you can't send response."})

        if not applicant.filter(program_to_join__direction=direction):
            raise serializers.ValidationError(
                {"detail": "Your response direction isn't appropriate for this stage, please fix it."}
            )

        return attrs


class StuffResponseDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StuffResponseDescription
        fields = "__all__"
