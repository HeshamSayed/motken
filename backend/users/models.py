"""
User models for Motken platform.
Supports Students, Teachers, and Admin users.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
import uuid


class UserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model supporting multiple user types."""

    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number format: '+999999999'")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # User Type
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')

    # Profile Information
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')

    # Language Preferences
    preferred_language = models.CharField(max_length=10, default='en', choices=[('en', 'English'), ('ar', 'Arabic')])

    # Account Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    # Biometric Authentication
    biometric_enabled = models.BooleanField(default=False)
    biometric_public_key = models.TextField(blank=True)

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    # For parental controls
    parent_email = models.EmailField(blank=True, help_text="Required for users under 18")
    requires_parental_consent = models.BooleanField(default=False)
    parental_consent_given = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the user's short name."""
        return self.first_name

    @property
    def is_student(self):
        """Check if user is a student."""
        return self.user_type == 'student'

    @property
    def is_teacher(self):
        """Check if user is a teacher."""
        return self.user_type == 'teacher'

    @property
    def is_admin_user(self):
        """Check if user is an admin."""
        return self.user_type == 'admin'


class StudentProfile(models.Model):
    """Extended profile for students."""

    LEARNING_GOAL_CHOICES = (
        ('reading', 'Learn to Read Quran'),
        ('tajweed', 'Master Tajweed'),
        ('memorization', 'Quran Memorization'),
        ('understanding', 'Understanding & Tafseer'),
        ('recitation', 'Improve Recitation'),
    )

    SKILL_LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')

    # Learning Preferences
    learning_goals = models.JSONField(default=list, help_text="List of learning goals")
    current_skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='beginner')
    preferred_teacher_gender = models.CharField(max_length=10, choices=User.GENDER_CHOICES, blank=True)

    # Session Preferences
    preferred_session_duration = models.IntegerField(default=30, help_text="Preferred session duration in minutes")
    preferred_days = models.JSONField(default=list, help_text="Preferred days of week")
    preferred_times = models.JSONField(default=list, help_text="Preferred time slots")

    # Progress Tracking
    total_sessions_completed = models.IntegerField(default=0)
    total_hours_learned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_curriculum = models.CharField(max_length=100, blank=True)
    current_lesson = models.CharField(max_length=100, blank=True)

    # Subscription Info
    current_package = models.CharField(max_length=50, blank=True)
    sessions_remaining = models.IntegerField(default=0)
    subscription_active = models.BooleanField(default=False)
    subscription_expires_at = models.DateTimeField(null=True, blank=True)

    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_ratings = models.IntegerField(default=0)

    # Notes
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_profiles'
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return f"Student: {self.user.get_full_name()}"


class DeviceToken(models.Model):
    """Store device tokens for push notifications."""

    PLATFORM_CHOICES = (
        ('ios', 'iOS'),
        ('android', 'Android'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'device_tokens'
        verbose_name = 'Device Token'
        verbose_name_plural = 'Device Tokens'
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.platform}"


class UserActivity(models.Model):
    """Track user activity and login history."""

    ACTION_CHOICES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Password Change'),
        ('profile_update', 'Profile Update'),
        ('session_booked', 'Session Booked'),
        ('payment_made', 'Payment Made'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activities'
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"
