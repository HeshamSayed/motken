"""
Admin configuration for Users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, StudentProfile, DeviceToken, UserActivity


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""

    list_display = ['email', 'get_full_name', 'user_type', 'is_active', 'is_verified', 'date_joined']
    list_filter = ['user_type', 'is_active', 'is_verified', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']

    fieldsets = (
        ('Authentication', {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'profile_picture', 'phone_number')
        }),
        ('User Type & Preferences', {
            'fields': ('user_type', 'preferred_language', 'country', 'timezone')
        }),
        ('Verification Status', {
            'fields': ('is_active', 'is_verified', 'email_verified', 'phone_verified')
        }),
        ('Security', {
            'fields': ('biometric_enabled', 'biometric_public_key')
        }),
        ('Parental Controls', {
            'fields': ('parent_email', 'requires_parental_consent', 'parental_consent_given')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'user_type'),
        }),
    )

    readonly_fields = ['date_joined', 'last_login']

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Admin interface for Student Profile."""

    list_display = ['user', 'current_skill_level', 'total_sessions_completed', 'subscription_active', 'average_rating']
    list_filter = ['current_skill_level', 'subscription_active', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['total_sessions_completed', 'total_hours_learned', 'average_rating', 'created_at', 'updated_at']

    fieldsets = (
        ('Student Information', {
            'fields': ('user',)
        }),
        ('Learning Preferences', {
            'fields': ('learning_goals', 'current_skill_level', 'preferred_teacher_gender')
        }),
        ('Session Preferences', {
            'fields': ('preferred_session_duration', 'preferred_days', 'preferred_times')
        }),
        ('Progress Statistics', {
            'fields': ('total_sessions_completed', 'total_hours_learned', 'current_curriculum', 'current_lesson')
        }),
        ('Subscription', {
            'fields': ('current_package', 'sessions_remaining', 'subscription_active', 'subscription_expires_at')
        }),
        ('Ratings', {
            'fields': ('average_rating', 'total_ratings')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    """Admin interface for Device Tokens."""

    list_display = ['user', 'platform', 'is_active', 'last_used']
    list_filter = ['platform', 'is_active', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['created_at', 'last_used']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin interface for User Activity."""

    list_display = ['user', 'action', 'timestamp', 'ip_address']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__email', 'ip_address']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
