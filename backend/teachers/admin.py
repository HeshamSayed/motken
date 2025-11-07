"""
Admin configuration for Teachers app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    TeacherProfile, TeacherAvailability, TeacherTimeOff,
    TeacherReview, TeacherCertification
)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    """Admin interface for Teacher Profile."""

    list_display = ['user', 'application_status', 'average_rating', 'total_sessions_taught', 'is_available', 'is_verified']
    list_filter = ['application_status', 'is_available', 'id_verified', 'background_check', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['application_date', 'total_sessions_taught', 'total_hours_taught',
                       'completion_rate', 'average_rating', 'total_ratings', 'created_at', 'updated_at']

    fieldsets = (
        ('Teacher Information', {
            'fields': ('user', 'application_status', 'application_date', 'approval_date', 'rejection_reason')
        }),
        ('Qualifications', {
            'fields': ('education', 'certifications', 'ijazah', 'ijazah_document', 'years_of_experience', 'specializations')
        }),
        ('Teaching Preferences', {
            'fields': ('teaching_styles', 'languages_spoken', 'can_teach_age_groups')
        }),
        ('Verification', {
            'fields': ('id_document', 'id_verified', 'background_check', 'background_check_date')
        }),
        ('Profile', {
            'fields': ('bio', 'introduction_video', 'teaching_methodology')
        }),
        ('Availability', {
            'fields': ('is_available', 'max_students', 'current_students')
        }),
        ('Statistics', {
            'fields': ('total_sessions_taught', 'total_hours_taught', 'completion_rate')
        }),
        ('Ratings', {
            'fields': ('average_rating', 'total_ratings', 'rating_breakdown')
        }),
        ('Pricing', {
            'fields': ('base_hourly_rate', 'session_30min_rate', 'session_45min_rate', 'session_60min_rate')
        }),
        ('Earnings', {
            'fields': ('total_earnings', 'pending_earnings', 'paid_earnings')
        }),
        ('Payment Information', {
            'fields': ('bank_account_number', 'bank_name', 'bank_account_holder', 'paypal_email')
        }),
        ('Featured Status', {
            'fields': ('is_featured', 'featured_until')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',)
        }),
    )

    actions = ['approve_teachers', 'reject_teachers', 'verify_teachers']

    def approve_teachers(self, request, queryset):
        updated = queryset.update(application_status='approved')
        self.message_user(request, f'{updated} teacher(s) approved.')
    approve_teachers.short_description = 'Approve selected teachers'

    def reject_teachers(self, request, queryset):
        updated = queryset.update(application_status='rejected')
        self.message_user(request, f'{updated} teacher(s) rejected.')
    reject_teachers.short_description = 'Reject selected teachers'

    def verify_teachers(self, request, queryset):
        updated = queryset.update(id_verified=True, background_check=True)
        self.message_user(request, f'{updated} teacher(s) verified.')
    verify_teachers.short_description = 'Verify selected teachers'


@admin.register(TeacherAvailability)
class TeacherAvailabilityAdmin(admin.ModelAdmin):
    """Admin interface for Teacher Availability."""

    list_display = ['teacher', 'day_of_week', 'start_time', 'end_time', 'is_active']
    list_filter = ['day_of_week', 'is_active']
    search_fields = ['teacher__user__email', 'teacher__user__first_name', 'teacher__user__last_name']


@admin.register(TeacherTimeOff)
class TeacherTimeOffAdmin(admin.ModelAdmin):
    """Admin interface for Teacher Time Off."""

    list_display = ['teacher', 'start_date', 'end_date', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['teacher__user__email', 'teacher__user__first_name', 'teacher__user__last_name']
    readonly_fields = ['created_at', 'updated_at']

    actions = ['approve_time_off', 'reject_time_off']

    def approve_time_off(self, request, queryset):
        updated = queryset.update(status='approved', approved_by=request.user)
        self.message_user(request, f'{updated} time-off request(s) approved.')
    approve_time_off.short_description = 'Approve selected time-off requests'

    def reject_time_off(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} time-off request(s) rejected.')
    reject_time_off.short_description = 'Reject selected time-off requests'


@admin.register(TeacherReview)
class TeacherReviewAdmin(admin.ModelAdmin):
    """Admin interface for Teacher Reviews."""

    list_display = ['teacher', 'student', 'overall_rating', 'is_approved', 'created_at']
    list_filter = ['overall_rating', 'is_approved', 'is_flagged', 'created_at']
    search_fields = ['teacher__user__email', 'student__email', 'review_text']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Review Information', {
            'fields': ('teacher', 'student', 'session')
        }),
        ('Ratings', {
            'fields': ('overall_rating', 'teaching_quality', 'communication', 'punctuality', 'patience')
        }),
        ('Review Content', {
            'fields': ('review_text', 'pros', 'cons')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_flagged', 'flagged_reason')
        }),
        ('Teacher Response', {
            'fields': ('teacher_response', 'response_date')
        }),
        ('Metadata', {
            'fields': ('is_verified_purchase', 'helpful_count', 'created_at', 'updated_at')
        }),
    )

    actions = ['approve_reviews', 'flag_reviews']

    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} review(s) approved.')
    approve_reviews.short_description = 'Approve selected reviews'

    def flag_reviews(self, request, queryset):
        updated = queryset.update(is_flagged=True)
        self.message_user(request, f'{updated} review(s) flagged.')
    flag_reviews.short_description = 'Flag selected reviews'


@admin.register(TeacherCertification)
class TeacherCertificationAdmin(admin.ModelAdmin):
    """Admin interface for Teacher Certifications."""

    list_display = ['teacher', 'certification_name', 'issuing_organization', 'is_verified', 'issue_date']
    list_filter = ['is_verified', 'issue_date']
    search_fields = ['teacher__user__email', 'certification_name', 'issuing_organization']
    readonly_fields = ['created_at', 'updated_at']

    actions = ['verify_certifications']

    def verify_certifications(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_verified=True, verified_by=request.user, verified_date=timezone.now().date())
        self.message_user(request, f'{updated} certification(s) verified.')
    verify_certifications.short_description = 'Verify selected certifications'
