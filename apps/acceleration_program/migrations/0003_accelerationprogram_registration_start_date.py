# Generated by Django 4.2 on 2023-04-24 08:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "acceleration_program",
            "0002_applicantresponse_applicants_joinprogram_stagetype_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="accelerationprogram",
            name="registration_start_date",
            field=models.DateField(default="2001-01-11"),
            preserve_default=False,
        ),
    ]
