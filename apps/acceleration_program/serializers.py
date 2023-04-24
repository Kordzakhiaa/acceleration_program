from rest_framework import serializers

from apps.acceleration_program.models import AccelerationProgram, JoinProgram, Applicants


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


class JoinProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinProgram
        fields = "__all__"


class RegisteredApplicantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicants
        fields = "__all__"
