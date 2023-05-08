# Generated by Django 4.2 on 2023-05-08 12:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("acceleration_program", "0003_alter_stuffresponsedescription_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stuffresponsedescription",
            name="status",
            field=models.CharField(
                choices=[
                    ("None", "None"),
                    ("Accepted", "Accepted"),
                    ("Rejected", "Rejected"),
                ],
                default="None",
                max_length=150,
            ),
        ),
    ]
