"""
Teacher models for Motken platform.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
import uuid


class TeacherProfile(models.Model):
    """Extended profile for teachers."""

    APPLICATION_STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    )

    TEACHING_STYLE_CHOICES = (
        ('structured', 'Structured & Formal'),
        ('casual', 'Casual & Friendly'),
        ('interactive', 'Interactive & Engaging'),
        ('patient', 'Patient & Supportive'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')

    # Application Status
    application_status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='pending')
    application_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    # Qualifications
    education = models.TextField(help_text="Educational background")
    certifications = models.JSONField(default=list, help_text="List of certifications")
    ijazah = models.BooleanField(default=False, help_text="Has Ijazah certificate")
    ijazah_document = models.FileField(upload_to='teacher_docs/ijazah/', null=True, blank=True)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0)])
    specializations = models.JSONField(default=list, help_text="Teaching specializations")

    # Teaching Preferences
    teaching_styles = models.JSONField(default=list, help_text="Preferred teaching styles")
    languages_spoken = models.JSONField(default=list, help_text="Languages the teacher speaks")
    can_teach_age_groups = models.JSONField(default=list, help_text="Age groups teacher can teach")

    # Verification Documents
    id_document = models.FileField(upload_to='teacher_docs/id/', null=True, blank=True)
    id_verified = models.BooleanField(default=False)
    background_check = models.BooleanField(default=False)
    background_check_date = models.DateField(null=True, blank=True)

    # Bio and Introduction
    bio = models.TextField(max_length=1000, help_text="Teacher biography")
    introduction_video = models.URLField(blank=True, help_text="Link to introduction video")
    teaching_methodology = models.TextField(blank=True)

    # Availability
    is_available = models.BooleanField(default=True)
    max_students = models.IntegerField(default=50, help_text="Maximum concurrent students")
    current_students = models.IntegerField(default=0)

    # Statistics
    total_sessions_taught = models.IntegerField(default=0)
    total_hours_taught = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Percentage")

    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_ratings = models.IntegerField(default=0)
    rating_breakdown = models.JSONField(default=dict, help_text="Star ratings breakdown")

    # Pricing (per session)
    base_hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    session_30min_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    session_45min_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    session_60min_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # Earnings
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Payment Information
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_holder = models.CharField(max_length=100, blank=True)
    paypal_email = models.EmailField(blank=True)

    # Featured & Premium
    is_featured = models.BooleanField(default=False)
    featured_until = models.DateTimeField(null=True, blank=True)

    # Admin Notes
    admin_notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teacher_profiles'
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'
        indexes = [
            models.Index(fields=['application_status']),
            models.Index(fields=['is_available']),
            models.Index(fields=['average_rating']),
        ]

    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"

    @property
    def is_verified(self):
        """Check if teacher is fully verified."""
        return (self.application_status == 'approved' and
                self.id_verified and
                self.background_check)

    @property
    def can_accept_students(self):
        """Check if teacher can accept new students."""
        return (self.is_available and
                self.is_verified and
                self.current_students < self.max_students)


class TeacherAvailability(models.Model):
    """Teacher availability schedule."""

    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_recurring = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    # For specific date overrides
    specific_date = models.DateField(null=True, blank=True, help_text="Override for specific date")

    class Meta:
        db_table = 'teacher_availability'
        verbose_name = 'Teacher Availability'
        verbose_name_plural = 'Teacher Availabilities'
        ordering = ['day_of_week', 'start_time']
        unique_together = ['teacher', 'day_of_week', 'start_time', 'end_time']

    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class TeacherTimeOff(models.Model):
    """Teacher time-off requests and approved leaves."""

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='time_off')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_time_offs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teacher_time_off'
        verbose_name = 'Teacher Time Off'
        verbose_name_plural = 'Teacher Time Offs'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.start_date.date()} to {self.end_date.date()}"


class TeacherReview(models.Model):
    """Student reviews for teachers."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_reviews')
    session = models.ForeignKey('sessions.Session', on_delete=models.SET_NULL, null=True, blank=True)

    # Ratings (1-5 stars)
    overall_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    teaching_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    punctuality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    patience = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Review Content
    review_text = models.TextField(max_length=1000)
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)

    # Moderation
    is_approved = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    flagged_reason = models.TextField(blank=True)

    # Teacher Response
    teacher_response = models.TextField(blank=True)
    response_date = models.DateTimeField(null=True, blank=True)

    # Metadata
    is_verified_purchase = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teacher_reviews'
        verbose_name = 'Teacher Review'
        verbose_name_plural = 'Teacher Reviews'
        ordering = ['-created_at']
        unique_together = ['teacher', 'student', 'session']
        indexes = [
            models.Index(fields=['teacher', '-created_at']),
            models.Index(fields=['is_approved']),
        ]

    def __str__(self):
        return f"Review for {self.teacher.user.get_full_name()} by {self.student.get_full_name()}"

    @property
    def average_category_rating(self):
        """Calculate average of all category ratings."""
        return (self.teaching_quality + self.communication +
                self.punctuality + self.patience) / 4


class TeacherCertification(models.Model):
    """Teacher certifications and qualifications."""

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='certification_details')
    certification_name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    document = models.FileField(upload_to='teacher_docs/certifications/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_certifications')
    verified_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teacher_certifications'
        verbose_name = 'Teacher Certification'
        verbose_name_plural = 'Teacher Certifications'
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.certification_name} - {self.teacher.user.get_full_name()}"
