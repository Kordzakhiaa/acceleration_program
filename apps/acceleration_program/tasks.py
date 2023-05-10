from datetime import datetime

from apps.acceleration_program.models import AccelerationProgram
from core.celery import app


@app.task
def check_acceleration_program() -> None:
    """
    Task that checks if program done or not.
    If acceleration program end date has come it must be disabled
    RESULT: AccelerationProgram.is_active=False
    """

    acceleration_program: "AccelerationProgram" = AccelerationProgram.objects.filter(is_active=True).first()
    if acceleration_program and acceleration_program.registration_end_date == datetime.now().date():
        acceleration_program.is_active = False
        acceleration_program.save()
