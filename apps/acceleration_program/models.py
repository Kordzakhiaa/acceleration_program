from django.db import models

from apps.directions.models import Direction


class AccelerationProgram(models.Model):
    directions = models.ManyToManyField(Direction)
    name = models.CharField(max_length=150)
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    program_start_time = models.DateField()
    program_end_time = models.DateField()

    registration_end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - active={self.is_active}"
