from typing import OrderedDict

from rest_framework import serializers

from apps.acceleration_program.models import (
    AccelerationProgram,
    JoinProgram,
    Applicants, Stage, OrderedStages,
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
    applicant = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Applicants
        fields = ["id", "applicant", "program_to_join"]

    def create(self, validated_data):
        applicant = Applicants(
            program_to_join=validated_data['program_to_join'],
            applicant=self.context['request'].user
        )
        applicant.save()
        return applicant


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = "__all__"


class OrderedStagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedStages
        fields = "__all__"


class OrderedStagesCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedStages
        fields = "__all__"

    def validate(self, attrs: "OrderedDict") -> "OrderedDict":
        """
        Method that validates stage.direction and join_program.direction to be same
        """
        join_program, stage = attrs.get("join_program"), attrs.get("stage")

        if stage.direction.id != join_program.direction.id:
            raise serializers.ValidationError({"detail": "Stage direction and JoinProgram direction must be the same."})

        return attrs
