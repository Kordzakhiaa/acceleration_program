from django.core.exceptions import ValidationError
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


class AssignmentType(models.Model):
    type = models.CharField(max_length=150)

    def __str__(self):
        return self.type


class Assignment(models.Model):
    type = models.ForeignKey(to=AssignmentType, on_delete=models.PROTECT)
    description = models.TextField(max_length=150)

    def __str__(self):
        return f"Assignment_Type={self.type}"


class Stage(models.Model):
    assignment = models.ForeignKey(to=Assignment, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"name={self.name}"


class JoinProgram(models.Model):
    program = models.ForeignKey(to=AccelerationProgram, on_delete=models.CASCADE)
    direction = models.ForeignKey(to=Direction, on_delete=models.PROTECT)

    applicants = models.ManyToManyField(to=CustomUserModel, through="Applicants")
    stages_data = models.ManyToManyField(to=Stage)

    joined_applicants = models.IntegerField(default=0)

    class Meta:
        unique_together = ["direction", "program"]

    def __str__(self):
        return f"direction={self.direction} - program={self.program}"


class Applicants(models.Model):
    class RequestStatuses(models.TextChoices):
        PENDING = _("Pending")
        ACCEPTED = _("Accepted")
        REJECTED = _("Rejected")

    program_to_join = models.ForeignKey(to=JoinProgram, on_delete=models.CASCADE, related_name="program_applicant")
    applicant = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE)

    join_request_date = models.DateTimeField(auto_now_add=True)
    request_status = models.CharField(max_length=150, default=RequestStatuses.PENDING, choices=RequestStatuses.choices)

    class Meta:
        unique_together = ["program_to_join", "applicant"]

    def __str__(self):
        return f"{self.applicant} - {self.program_to_join}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.program_to_join.joined_applicants += 1
            self.program_to_join.save()
        super().save(*args, **kwargs)


class ApplicantResponse(models.Model):
    class Statuses(models.TextChoices):
        PENDING = _("Pending")
        ACCEPTED = _("Accepted")
        REJECTED = _("Rejected")

    applicant = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE)
    stage = models.ForeignKey(to=Stage, on_delete=models.CASCADE)
    direction = models.ForeignKey(to=Direction, on_delete=models.CASCADE)

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
        REJECTED = _("Rejected")

    author = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE)
    applicant_response = models.ForeignKey(to=ApplicantResponse, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=150, default=Statuses.NONE, choices=Statuses.choices)

    class Meta:
        unique_together = ["author", "applicant_response"]

    def __str__(self):
        return f"author={self.author} - {self.status}"

    def clean(self):
        """Method that raises exception (DJANGO ADMIN INTERFACE) if author isn't admin or stuff-direction"""
        if self.author.user_type not in ["Stuff-Direction", "Admin"]:
            raise ValidationError("Author must be Stuff-Direction or Admin user")
