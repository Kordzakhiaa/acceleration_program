import json
from datetime import date
from typing import OrderedDict

from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework import serializers

from apps.acceleration_program.models import (
    AccelerationProgram,
    JoinProgram,
    Applicants,
    Stage,
    ApplicantResponse,
    StuffFinalResponseDescription,
    StuffMembersResponse,
)


class AccelerationProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccelerationProgram
        fields = [
            "id",
            "name",
            "requirements",
            "directions",
            "program_start_date",
            "program_end_date",
            "registration_start_date",
            "registration_end_date",
            "is_active",
        ]

    def validate(self, attrs: "OrderedDict") -> "OrderedDict":
        """
        Method that validates AccelerationProgram instance based on name and status
        and after validation it creates clocked schedule and periodic task based on
        the acceleration program's registration_end_date
        ---------------------------------------------------------------------------
        E.g:
            {
                "name": "Test Acceleration Program",
                "registration_end_date": "2020-01-01"
                ...
            }
            If the data with the same body is in DATABASE, it will raise an exception with status 400_BAD_REQUEST
            If everything is OK it will create ClockedSchedule and PeriodicTask based on registration_end_date
            using __create_clocked_scheduled_periodic_task-method and when time will come it will set status of this
            acceleration program to False so after that no-one can register on this program
        """

        name, status, program_start_date, program_end_date, registration_start_date, registration_end_date = (
            attrs.get("name"),
            attrs.get("is_active"),
            attrs.get("program_start_date"),
            attrs.get("program_end_date"),
            attrs.get("registration_start_date"),
            attrs.get("registration_end_date"),
        )

        if AccelerationProgram.objects.filter(name=name, is_active=True):
            raise serializers.ValidationError({"detail": "Active acceleration program with this name already exists"})

        if program_start_date > program_end_date:
            raise serializers.ValidationError({"detail": "Program start date must be less than program end date"})

        if program_start_date <= registration_start_date or program_start_date < registration_end_date:
            raise serializers.ValidationError(
                {"detail": "Program start date must be higher than registration start date and registration end date"}
            )
        if program_end_date <= registration_end_date:
            raise serializers.ValidationError({"detail": "Program end time must be less than registration end date"})

        if registration_start_date >= registration_end_date:
            raise serializers.ValidationError(
                {"detail": "Registration start date must be less than registration end date"}
            )

        self._create_clocked_scheduled_periodic_task(name=name, registration_end_date=registration_end_date)

        return attrs

    @staticmethod
    def create_joinprogram_template(instance: "AccelerationProgram") -> None:  # noqa
        """
        After calling this method templates of JoinProgram should be created based on chosen direction
        """

        for direction in instance.directions.all():
            JoinProgram.objects.update_or_create(program_id=instance.id, direction=direction)

    @staticmethod
    def _create_clocked_scheduled_periodic_task(*, name: str, registration_end_date: date) -> None:
        clocked_schedule, _ = ClockedSchedule.objects.update_or_create(
            clocked_time=registration_end_date,
        )

        PeriodicTask.objects.update_or_create(
            clocked=clocked_schedule,
            name=f"Periodic task for program -> {name}",
            task="apps.acceleration_program.tasks.check_acceleration_program",
            args=json.dumps([name]),
            one_off=True,
        )


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


class ApplicantResponseSerializer(serializers.ModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ApplicantResponse
        fields = ["id", "applicant", "stage", "direction", "applicant_response_description"]

    def validate(self, attrs: "OrderedDict") -> "OrderedDict":
        """
        Method that validates API call in different ways
        ------------------------------------------------
        RESPONSE WITH STATUS 400_BAD_REQUEST in cases when:
        1) Request user isn't registered as an applicant
        2) When stage exists but for program it isn't selected(registered) yet
        3) User request to register as an applicant is PENDING or REJECTED
        4) When direction of this program isn't appropriate
        5) In previous stage of the program the applicant response where REJECTED
        """

        user_id = self.context.get("request").user.id
        stage: Stage = attrs.get("stage")
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

        if Stage.objects.filter(
            joinprogram__program__is_active=True,
            applicantresponse__applicant=user_id,
            applicantresponse__status="Rejected",
        ):
            raise serializers.ValidationError(
                {"detail": "You are rejected in previous stage, therefore you can't send response."}
            )

        return attrs


class StuffFinalResponseDescriptionSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = StuffFinalResponseDescription
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

        if status == "None":
            raise serializers.ValidationError(
                {"detail": "Status must be accepted or rejected, please use one of them."}
            )
        applicant_response.status = status
        applicant_response.save()

        return attrs


class StuffMembersResponseSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = StuffMembersResponse
        fields = ["id", "author", "point", "applicant_response"]
