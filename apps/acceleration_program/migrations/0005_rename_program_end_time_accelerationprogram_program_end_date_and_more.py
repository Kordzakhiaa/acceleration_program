# Generated by Django 4.2 on 2023-05-10 18:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("acceleration_program", "0004_alter_stuffresponsedescription_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="accelerationprogram",
            old_name="program_end_time",
            new_name="program_end_date",
        ),
        migrations.RenameField(
            model_name="accelerationprogram",
            old_name="program_start_time",
            new_name="program_start_date",
        ),
    ]