"""
Celery tasks for payments.
"""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import TeacherPayout, Subscription
from sessions.models import Session


@shared_task
def process_teacher_payouts():
    """
    Process monthly teacher payouts.
    Runs on the 1st of each month.
    """
    from teachers.models import TeacherProfile

    # Get last month's date range
    today = timezone.now().date()
    first_of_month = today.replace(day=1)
    last_month_end = first_of_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    processed_count = 0
    total_amount = Decimal('0.00')

    # Get all active teachers
    teachers = TeacherProfile.objects.filter(
        application_status='approved',
        pending_earnings__gt=0
    )

    for teacher in teachers:
        # Get completed sessions from last month
        sessions = Session.objects.filter(
            teacher=teacher,
            status='completed',
            scheduled_date__gte=last_month_start,
            scheduled_date__lte=last_month_end
        )

        if not sessions.exists():
            continue

        # Calculate total payout
        payout_amount = sum(session.teacher_payout for session in sessions)

        # Create payout record
        payout = TeacherPayout.objects.create(
            teacher=teacher,
            amount=payout_amount,
            currency='USD',
            payout_method='bank_transfer',  # Default
            status='pending',
            period_start=last_month_start,
            period_end=last_month_end,
            session_count=sessions.count(),
            bank_account=teacher.bank_account_number,
            paypal_email=teacher.paypal_email
        )

        # Add sessions to payout
        payout.sessions.set(sessions)

        # Update teacher earnings
        teacher.pending_earnings -= payout_amount
        teacher.save()

        processed_count += 1
        total_amount += payout_amount

    return {
        'processed_count': processed_count,
        'total_amount': float(total_amount)
    }


@shared_task
def check_expiring_subscriptions():
    """
    Check for subscriptions expiring in 7 days and send reminders.
    """
    seven_days_from_now = timezone.now().date() + timedelta(days=7)

    expiring_subscriptions = Subscription.objects.filter(
        status='active',
        end_date=seven_days_from_now,
        auto_renew=False
    )

    for subscription in expiring_subscriptions:
        # TODO: Send notification to user
        print(f"Subscription {subscription.id} expiring soon for {subscription.student.email}")

    return {'expiring_count': expiring_subscriptions.count()}


@shared_task
def auto_renew_subscriptions():
    """
    Automatically renew subscriptions with auto_renew enabled.
    """
    today = timezone.now().date()

    subscriptions_to_renew = Subscription.objects.filter(
        status='active',
        auto_renew=True,
        renewal_date=today
    )

    renewed_count = 0

    for subscription in subscriptions_to_renew:
        # TODO: Process payment for renewal
        # TODO: Create new subscription or extend current one

        # For now, just extend the subscription
        subscription.end_date = subscription.end_date + timedelta(days=subscription.package.validity_days)
        subscription.sessions_remaining += subscription.package.session_count
        subscription.total_sessions += subscription.package.session_count
        subscription.renewal_date = subscription.end_date
        subscription.save()

        renewed_count += 1

    return {'renewed_count': renewed_count}


@shared_task
def expire_old_subscriptions():
    """
    Mark expired subscriptions as expired.
    """
    today = timezone.now().date()

    expired = Subscription.objects.filter(
        status='active',
        end_date__lt=today
    ).update(status='expired')

    return {'expired_count': expired}
