"""
Session serializers for API.
"""

from rest_framework import serializers
from .models import (
    Session, SessionProgress, SessionAttachment, SessionMessage,
    SessionRating, BookingRequest
)
from users.serializers import UserSerializer
from teachers.serializers import TeacherListSerializer


class SessionSerializer(serializers.ModelSerializer):
    """Serializer for Session."""

    student = UserSerializer(read_only=True)
    teacher = TeacherListSerializer(read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    can_cancel = serializers.BooleanField(read_only=True)

    class Meta:
        model = Session
        fields = [
            'id', 'student', 'teacher', 'scheduled_date', 'scheduled_time',
            'duration', 'end_time', 'curriculum', 'lesson_topic', 'session_goals',
            'status', 'zoom_meeting_id', 'zoom_meeting_password', 'zoom_join_url',
            'zoom_start_url', 'actual_start_time', 'actual_end_time', 'actual_duration',
            'session_recording_url', 'recording_available', 'teacher_notes',
            'student_notes', 'homework_assigned', 'homework_completed',
            'cancellation_reason', 'cancelled_at', 'session_price', 'teacher_payout',
            'platform_fee', 'is_recurring', 'is_trial', 'created_at', 'is_upcoming',
            'can_cancel'
        ]
        read_only_fields = [
            'id', 'zoom_meeting_id', 'zoom_meeting_password', 'zoom_join_url',
            'zoom_start_url', 'actual_start_time', 'actual_end_time', 'actual_duration',
            'session_recording_url', 'recording_available', 'session_price',
            'teacher_payout', 'platform_fee', 'created_at'
        ]


class SessionBookingSerializer(serializers.Serializer):
    """Serializer for booking a session."""

    teacher = serializers.UUIDField()
    scheduled_date = serializers.DateField()
    scheduled_time = serializers.TimeField()
    duration = serializers.ChoiceField(choices=[30, 45, 60])
    curriculum = serializers.CharField(max_length=100, required=False, allow_blank=True)
    lesson_topic = serializers.CharField(max_length=200, required=False, allow_blank=True)
    session_goals = serializers.CharField(required=False, allow_blank=True)
    is_trial = serializers.BooleanField(default=False)

    def validate(self, attrs):
        from teachers.models import TeacherProfile
        from datetime import datetime, timedelta
        from django.utils import timezone

        # Check if teacher exists and is available
        try:
            teacher = TeacherProfile.objects.get(id=attrs['teacher'])
        except TeacherProfile.DoesNotExist:
            raise serializers.ValidationError({"teacher": "Teacher not found."})

        if not teacher.is_available:
            raise serializers.ValidationError({"teacher": "Teacher is not currently accepting bookings."})

        # Check if date/time is in the future
        session_datetime = datetime.combine(attrs['scheduled_date'], attrs['scheduled_time'])
        session_datetime = timezone.make_aware(session_datetime)

        if session_datetime <= timezone.now():
            raise serializers.ValidationError({"scheduled_date": "Session must be scheduled in the future."})

        # Check if at least 24 hours in advance
        if session_datetime < timezone.now() + timedelta(hours=24):
            raise serializers.ValidationError({"scheduled_date": "Session must be booked at least 24 hours in advance."})

        attrs['teacher_obj'] = teacher
        return attrs


class SessionProgressSerializer(serializers.ModelSerializer):
    """Serializer for Session Progress."""

    class Meta:
        model = SessionProgress
        fields = [
            'id', 'session', 'surah_covered', 'ayah_from', 'ayah_to', 'juz_covered',
            'pronunciation_score', 'tajweed_score', 'memorization_score', 'overall_score',
            'skills_improved', 'areas_to_improve', 'next_lesson_plan',
            'recommended_practice', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SessionAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for Session Attachments."""

    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = SessionAttachment
        fields = [
            'id', 'session', 'uploaded_by', 'file', 'file_name',
            'file_type', 'file_size', 'description', 'created_at'
        ]
        read_only_fields = ['id', 'file_size', 'created_at']


class SessionMessageSerializer(serializers.ModelSerializer):
    """Serializer for Session Messages."""

    sender = UserSerializer(read_only=True)

    class Meta:
        model = SessionMessage
        fields = [
            'id', 'session', 'sender', 'message', 'is_read',
            'read_at', 'attachment', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'is_read', 'read_at', 'created_at']


class SessionRatingSerializer(serializers.ModelSerializer):
    """Serializer for Session Ratings."""

    student = UserSerializer(read_only=True)

    class Meta:
        model = SessionRating
        fields = [
            'id', 'session', 'student', 'overall_rating', 'teaching_quality',
            'session_value', 'feedback', 'would_recommend', 'created_at'
        ]
        read_only_fields = ['id', 'student', 'created_at']

    def validate(self, attrs):
        rating_fields = ['overall_rating', 'teaching_quality', 'session_value']
        for field in rating_fields:
            if field in attrs and (attrs[field] < 1 or attrs[field] > 5):
                raise serializers.ValidationError({field: "Rating must be between 1 and 5."})
        return attrs


class BookingRequestSerializer(serializers.ModelSerializer):
    """Serializer for Booking Requests."""

    student = UserSerializer(read_only=True)
    teacher = TeacherListSerializer(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = BookingRequest
        fields = [
            'id', 'student', 'teacher', 'requested_date', 'requested_time',
            'duration', 'message', 'learning_goals', 'status', 'response_message',
            'responded_at', 'session', 'created_at', 'expires_at', 'is_expired'
        ]
        read_only_fields = [
            'id', 'student', 'status', 'response_message', 'responded_at',
            'session', 'created_at', 'expires_at'
        ]
