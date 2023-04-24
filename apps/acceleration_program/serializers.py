from typing import OrderedDict

from rest_framework import serializers

from apps.acceleration_program.models import (
    AccelerationProgram,
    JoinProgram,
    Applicants,
)


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
    class Meta:
        model = Applicants
        fields = ["id", "program_to_join"]

    def validate(self, attrs):
        applicant = attrs.get("applicant")
        program_to_join = attrs.get("program_to_join")
        Applicants.objects.create(applicant=applicant, program_to_join=program_to_join)

        return attrs
