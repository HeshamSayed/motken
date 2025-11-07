"""
Celery configuration for Motken project.
"""

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('motken')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'send-session-reminders': {
        'task': 'sessions.tasks.send_session_reminders',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'process-teacher-payouts': {
        'task': 'payments.tasks.process_teacher_payouts',
        'schedule': crontab(hour=0, minute=0, day_of_month=1),  # Monthly
    },
    'cleanup-expired-sessions': {
        'task': 'sessions.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
