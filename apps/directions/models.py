from django.db import models


class Direction(models.Model):
    title = models.CharField(max_length=150)
    number_of_stages = models.IntegerField()

    def __str__(self):
        return self.title
