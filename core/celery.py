import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every day at 00:01
    'check-every-day': {
        'task': 'apps.acceleration_program.tasks.check_acceleration_program',
        'schedule': crontab(hour=24),
    },
}
