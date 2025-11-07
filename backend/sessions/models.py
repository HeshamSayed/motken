"""
Session models for Motken platform.
Handles session booking, scheduling, and management.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from users.models import User
from teachers.models import TeacherProfile
import uuid


class Session(models.Model):
    """Main session model."""

    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled_by_student', 'Cancelled by Student'),
        ('cancelled_by_teacher', 'Cancelled by Teacher'),
        ('cancelled_by_admin', 'Cancelled by Admin'),
        ('no_show_student', 'Student No-Show'),
        ('no_show_teacher', 'Teacher No-Show'),
        ('rescheduled', 'Rescheduled'),
    )

    DURATION_CHOICES = (
        (30, '30 minutes'),
        (45, '45 minutes'),
        (60, '60 minutes'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Participants
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_sessions')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='teaching_sessions')

    # Schedule
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    duration = models.IntegerField(choices=DURATION_CHOICES, default=30)
    end_time = models.TimeField(null=True, blank=True)

    # Session Details
    curriculum = models.CharField(max_length=100, blank=True)
    lesson_topic = models.CharField(max_length=200, blank=True)
    session_goals = models.TextField(blank=True)

    # Status
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='scheduled')

    # Video Call
    zoom_meeting_id = models.CharField(max_length=100, blank=True)
    zoom_meeting_password = models.CharField(max_length=50, blank=True)
    zoom_join_url = models.URLField(blank=True)
    zoom_start_url = models.URLField(blank=True)

    # Session Completion
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    actual_duration = models.IntegerField(null=True, blank=True, help_text="Actual duration in minutes")

    # Recording
    session_recording_url = models.URLField(blank=True)
    recording_available = models.BooleanField(default=False)
    recording_password = models.CharField(max_length=50, blank=True)

    # Notes and Feedback
    teacher_notes = models.TextField(blank=True)
    student_notes = models.TextField(blank=True)
    homework_assigned = models.TextField(blank=True)
    homework_completed = models.BooleanField(default=False)

    # Cancellation
    cancellation_reason = models.TextField(blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_sessions')

    # Pricing
    session_price = models.DecimalField(max_digits=8, decimal_places=2)
    teacher_payout = models.DecimalField(max_digits=8, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=8, decimal_places=2)

    # Reminders
    reminder_sent = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)

    # Recurring Session
    is_recurring = models.BooleanField(default=False)
    recurring_pattern = models.CharField(max_length=50, blank=True, help_text="e.g., 'weekly', 'biweekly'")
    recurring_parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='recurring_children')

    # Trial Session
    is_trial = models.BooleanField(default=False)
    trial_discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sessions'
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        ordering = ['-scheduled_date', '-scheduled_time']
        indexes = [
            models.Index(fields=['student', '-scheduled_date']),
            models.Index(fields=['teacher', '-scheduled_date']),
            models.Index(fields=['status']),
            models.Index(fields=['scheduled_date', 'scheduled_time']),
        ]

    def __str__(self):
        return f"Session: {self.student.get_full_name()} with {self.teacher.user.get_full_name()} on {self.scheduled_date}"

    @property
    def is_upcoming(self):
        """Check if session is upcoming."""
        now = timezone.now()
        session_datetime = timezone.make_aware(
            timezone.datetime.combine(self.scheduled_date, self.scheduled_time)
        )
        return session_datetime > now and self.status == 'scheduled'

    @property
    def is_past(self):
        """Check if session is in the past."""
        now = timezone.now()
        session_datetime = timezone.make_aware(
            timezone.datetime.combine(self.scheduled_date, self.scheduled_time)
        )
        return session_datetime < now

    @property
    def can_cancel(self):
        """Check if session can be cancelled (24 hours before)."""
        now = timezone.now()
        session_datetime = timezone.make_aware(
            timezone.datetime.combine(self.scheduled_date, self.scheduled_time)
        )
        hours_until_session = (session_datetime - now).total_seconds() / 3600
        return hours_until_session >= 24 and self.status == 'scheduled'


class SessionProgress(models.Model):
    """Track progress within a session or across sessions."""

    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='progress')

    # Quran Progress
    surah_covered = models.CharField(max_length=100, blank=True)
    ayah_from = models.IntegerField(null=True, blank=True)
    ayah_to = models.IntegerField(null=True, blank=True)
    juz_covered = models.IntegerField(null=True, blank=True)

    # Performance Metrics
    pronunciation_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    tajweed_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    memorization_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    overall_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Skills Assessment
    skills_improved = models.JSONField(default=list, help_text="List of skills improved")
    areas_to_improve = models.JSONField(default=list, help_text="List of areas needing improvement")

    # Next Steps
    next_lesson_plan = models.TextField(blank=True)
    recommended_practice = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'session_progress'
        verbose_name = 'Session Progress'
        verbose_name_plural = 'Session Progress'

    def __str__(self):
        return f"Progress for session {self.session.id}"


class SessionAttachment(models.Model):
    """Attachments shared during sessions."""

    ATTACHMENT_TYPE_CHOICES = (
        ('document', 'Document'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attachments')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    file = models.FileField(upload_to='session_attachments/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPE_CHOICES)
    file_size = models.IntegerField(help_text="File size in bytes")
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'session_attachments'
        verbose_name = 'Session Attachment'
        verbose_name_plural = 'Session Attachments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.file_name} - {self.session.id}"


class SessionMessage(models.Model):
    """Messages/chat during sessions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    # Attachments
    attachment = models.FileField(upload_to='session_messages/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'session_messages'
        verbose_name = 'Session Message'
        verbose_name_plural = 'Session Messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
        ]

    def __str__(self):
        return f"Message from {self.sender.get_full_name()} in session {self.session.id}"


class SessionRating(models.Model):
    """Student rating for completed sessions."""

    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='rating')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_ratings')

    # Ratings (1-5 stars)
    overall_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    teaching_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    session_value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Feedback
    feedback = models.TextField(max_length=500, blank=True)
    would_recommend = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'session_ratings'
        verbose_name = 'Session Rating'
        verbose_name_plural = 'Session Ratings'

    def __str__(self):
        return f"Rating for session {self.session.id} - {self.overall_rating} stars"


class BookingRequest(models.Model):
    """Booking requests from students to teachers."""

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_requests')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='booking_requests')

    # Requested Schedule
    requested_date = models.DateField()
    requested_time = models.TimeField()
    duration = models.IntegerField(choices=Session.DURATION_CHOICES)

    # Details
    message = models.TextField(blank=True)
    learning_goals = models.TextField(blank=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response_message = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    # If accepted, link to created session
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="Request expires after 48 hours")

    class Meta:
        db_table = 'booking_requests'
        verbose_name = 'Booking Request'
        verbose_name_plural = 'Booking Requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['teacher', 'status']),
        ]

    def __str__(self):
        return f"Booking request from {self.student.get_full_name()} to {self.teacher.user.get_full_name()}"

    @property
    def is_expired(self):
        """Check if booking request has expired."""
        return timezone.now() > self.expires_at and self.status == 'pending'
