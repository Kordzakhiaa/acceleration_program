from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUserModel
from apps.directions.models import Direction


class AccelerationProgram(models.Model):
    directions = models.ManyToManyField(Direction)
    name = models.CharField(max_length=150)
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    program_start_time = models.DateField()
    program_end_time = models.DateField()

    registration_start_date = models.DateField()
    registration_end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - active={self.is_active}"

    def save(self, *args, **kwargs):
        """
        Overriding save method to ensure that after calling save,
        templates of JoinProgram should be created based on chosen direction
        """
        super().save(*args, **kwargs)
        for direction in self.directions.all():
            JoinProgram.objects.update_or_create(program=self, direction=direction)


class StageType(models.Model):
    class StageTypes(models.TextChoices):
        TEST = _("Test")
        TASK = _("Task")
        LIVE_CODING = _("Live Coding")
        INTERVIEW = _("Interview")

    type = models.CharField(max_length=150, choices=StageTypes.choices)

    def __str__(self):
        return self.type


class Stage(models.Model):
    direction = models.ForeignKey(to=Direction, on_delete=models.PROTECT)
    type = models.ForeignKey(to=StageType, on_delete=models.PROTECT)

    name = models.CharField(max_length=150)
    assigment_with_description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class JoinProgram(models.Model):
    program = models.ForeignKey(to=AccelerationProgram, on_delete=models.CASCADE)
    direction = models.ForeignKey(to=Direction, on_delete=models.PROTECT)

    applicants = models.ManyToManyField(to=CustomUserModel, through="Applicants")
    stages_data = models.ManyToManyField(to=Stage, through="OrderedStages")

    joined_applicants = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ["direction", "program"]

    def __str__(self):
        return f"direction={self.direction} - program={self.program}"


class OrderedStages(models.Model):
    join_program = models.ForeignKey(to=JoinProgram, on_delete=models.CASCADE)
    stage = models.ForeignKey(to=Stage, on_delete=models.CASCADE)

    stage_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ["join_program", "stage"]


class Applicants(models.Model):
    class RequestStatuses(models.TextChoices):
        PENDING = _("Pending")
        ACCEPTED = _("Accepted")
        REJECTED = _("Rejected")

    program_to_join = models.ForeignKey(to=JoinProgram, on_delete=models.CASCADE, related_name="program_applicant")
    applicant = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE)

    join_request_date = models.DateTimeField(auto_now_add=True)
    request_status = models.CharField(max_length=150, default=RequestStatuses.PENDING, choices=RequestStatuses.choices)

    def __str__(self):
        return f"{self.applicant} - {self.program_to_join}"


class ApplicantResponse(models.Model):
    class Statuses(models.TextChoices):
        PENDING = _("Pending")
        ACCEPTED = _("Accepted")
        REJECTED = _("Rejected")

    applicant = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE)
    stage = models.ForeignKey(to=Stage, on_delete=models.CASCADE)

    applicant_response_description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=150, default=Statuses.PENDING, choices=Statuses.choices)

    class Meta:
        unique_together = ["applicant", "stage"]

    def __str__(self):
        return f"{self.applicant} - {self.stage} - {self.status}"


class StuffResponseDescription(models.Model):
    class Statuses(models.TextChoices):
        NONE = _("None")
        ACCEPTED = _("Accepted")
        MAYBE = _("Maybe")
        REJECTED = _("Rejected")

    author = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE)
    applicant_response = models.ForeignKey(to=ApplicantResponse, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=150, default=Statuses.NONE, choices=Statuses.choices)
