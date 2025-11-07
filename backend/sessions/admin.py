"""
Admin configuration for Sessions app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Session, SessionProgress, SessionAttachment, SessionMessage,
    SessionRating, BookingRequest
)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Admin interface for Sessions."""

    list_display = ['id', 'student', 'teacher', 'scheduled_date', 'scheduled_time', 'duration', 'status']
    list_filter = ['status', 'duration', 'is_trial', 'scheduled_date']
    search_fields = ['student__email', 'teacher__user__email', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'actual_duration']
    date_hierarchy = 'scheduled_date'

    fieldsets = (
        ('Participants', {
            'fields': ('student', 'teacher')
        }),
        ('Schedule', {
            'fields': ('scheduled_date', 'scheduled_time', 'duration', 'end_time')
        }),
        ('Session Details', {
            'fields': ('curriculum', 'lesson_topic', 'session_goals', 'status')
        }),
        ('Video Call', {
            'fields': ('zoom_meeting_id', 'zoom_meeting_password', 'zoom_join_url', 'zoom_start_url')
        }),
        ('Completion', {
            'fields': ('actual_start_time', 'actual_end_time', 'actual_duration')
        }),
        ('Recording', {
            'fields': ('session_recording_url', 'recording_available', 'recording_password')
        }),
        ('Notes & Feedback', {
            'fields': ('teacher_notes', 'student_notes', 'homework_assigned', 'homework_completed')
        }),
        ('Cancellation', {
            'fields': ('cancellation_reason', 'cancelled_at', 'cancelled_by')
        }),
        ('Pricing', {
            'fields': ('session_price', 'teacher_payout', 'platform_fee')
        }),
        ('Recurring Session', {
            'fields': ('is_recurring', 'recurring_pattern', 'recurring_parent')
        }),
        ('Trial', {
            'fields': ('is_trial', 'trial_discount_percent')
        }),
    )

    actions = ['mark_completed', 'cancel_sessions']

    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} session(s) marked as completed.')
    mark_completed.short_description = 'Mark selected sessions as completed'

    def cancel_sessions(self, request, queryset):
        updated = queryset.update(status='cancelled_by_admin', cancelled_by=request.user)
        self.message_user(request, f'{updated} session(s) cancelled.')
    cancel_sessions.short_description = 'Cancel selected sessions'


@admin.register(SessionProgress)
class SessionProgressAdmin(admin.ModelAdmin):
    """Admin interface for Session Progress."""

    list_display = ['session', 'surah_covered', 'overall_score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['session__id', 'surah_covered']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SessionAttachment)
class SessionAttachmentAdmin(admin.ModelAdmin):
    """Admin interface for Session Attachments."""

    list_display = ['file_name', 'session', 'uploaded_by', 'file_type', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['file_name', 'session__id']
    readonly_fields = ['id', 'created_at']


@admin.register(SessionMessage)
class SessionMessageAdmin(admin.ModelAdmin):
    """Admin interface for Session Messages."""

    list_display = ['sender', 'session', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__email', 'message', 'session__id']
    readonly_fields = ['id', 'created_at']


@admin.register(SessionRating)
class SessionRatingAdmin(admin.ModelAdmin):
    """Admin interface for Session Ratings."""

    list_display = ['session', 'student', 'overall_rating', 'would_recommend', 'created_at']
    list_filter = ['overall_rating', 'would_recommend', 'created_at']
    search_fields = ['session__id', 'student__email']
    readonly_fields = ['created_at']


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    """Admin interface for Booking Requests."""

    list_display = ['student', 'teacher', 'requested_date', 'requested_time', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['student__email', 'teacher__user__email']
    readonly_fields = ['id', 'created_at', 'expires_at']

    actions = ['accept_requests', 'reject_requests']

    def accept_requests(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f'{updated} booking request(s) accepted.')
    accept_requests.short_description = 'Accept selected booking requests'

    def reject_requests(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} booking request(s) rejected.')
    reject_requests.short_description = 'Reject selected booking requests'
