"""
Celery tasks for sessions.
"""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Session


@shared_task
def send_session_reminders():
    """Send session reminders 24 hours and 1 hour before session."""

    now = timezone.now()

    # 24 hour reminders
    start_24h = now + timedelta(hours=23, minutes=45)
    end_24h = now + timedelta(hours=24, minutes=15)

    sessions_24h = Session.objects.filter(
        scheduled_date__gte=start_24h.date(),
        scheduled_date__lte=end_24h.date(),
        status='scheduled',
        reminder_sent=False
    )

    for session in sessions_24h:
        # TODO: Send push notification and email
        print(f"Sending 24h reminder for session {session.id}")
        session.reminder_sent = True
        session.reminder_sent_at = now
        session.save()

    # 1 hour reminders
    start_1h = now + timedelta(minutes=45)
    end_1h = now + timedelta(hours=1, minutes=15)

    sessions_1h = Session.objects.filter(
        scheduled_date__gte=start_1h.date(),
        scheduled_date__lte=end_1h.date(),
        status='scheduled'
    )

    for session in sessions_1h:
        # TODO: Send push notification
        print(f"Sending 1h reminder for session {session.id}")

    return {
        'reminders_24h': sessions_24h.count(),
        'reminders_1h': sessions_1h.count()
    }


@shared_task
def cleanup_expired_sessions():
    """Clean up old completed/cancelled sessions."""

    cutoff_date = timezone.now() - timedelta(days=90)

    sessions = Session.objects.filter(
        status__in=['completed', 'cancelled_by_student', 'cancelled_by_teacher'],
        updated_at__lt=cutoff_date
    )

    count = sessions.count()
    # Archive instead of delete
    # sessions.delete()

    return {'cleaned_sessions': count}
