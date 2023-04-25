# Generated by Django 4.2 on 2023-04-25 07:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("acceleration_program", "0004_alter_joinprogram_applicants_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="applicants",
            unique_together={("program_to_join", "applicant")},
        ),
    ]
