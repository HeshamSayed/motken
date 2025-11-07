"""
Teacher serializers for API.
"""

from rest_framework import serializers
from .models import (
    TeacherProfile, TeacherAvailability, TeacherTimeOff,
    TeacherReview, TeacherCertification
)
from users.serializers import UserSerializer


class TeacherProfileSerializer(serializers.ModelSerializer):
    """Serializer for Teacher Profile."""

    user = UserSerializer(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    can_accept_students = serializers.BooleanField(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'user', 'application_status', 'application_date', 'approval_date',
            'education', 'certifications', 'ijazah', 'ijazah_document',
            'years_of_experience', 'specializations', 'teaching_styles',
            'languages_spoken', 'can_teach_age_groups', 'id_document',
            'id_verified', 'background_check', 'bio', 'introduction_video',
            'teaching_methodology', 'is_available', 'max_students', 'current_students',
            'total_sessions_taught', 'total_hours_taught', 'completion_rate',
            'average_rating', 'total_ratings', 'rating_breakdown',
            'session_30min_rate', 'session_45min_rate', 'session_60min_rate',
            'is_featured', 'featured_until', 'is_verified', 'can_accept_students'
        ]
        read_only_fields = [
            'id', 'application_status', 'application_date', 'approval_date',
            'id_verified', 'background_check', 'total_sessions_taught',
            'total_hours_taught', 'completion_rate', 'average_rating',
            'total_ratings', 'rating_breakdown', 'is_featured', 'featured_until'
        ]


class TeacherListSerializer(serializers.ModelSerializer):
    """Simplified serializer for teacher list."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'user', 'specializations', 'years_of_experience',
            'average_rating', 'total_ratings', 'session_30min_rate',
            'session_45min_rate', 'session_60min_rate', 'is_available',
            'is_featured', 'bio'
        ]


class TeacherAvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for Teacher Availability."""

    class Meta:
        model = TeacherAvailability
        fields = [
            'id', 'day_of_week', 'start_time', 'end_time',
            'is_recurring', 'is_active', 'specific_date'
        ]
        read_only_fields = ['id']


class TeacherTimeOffSerializer(serializers.ModelSerializer):
    """Serializer for Teacher Time Off."""

    teacher = TeacherProfileSerializer(read_only=True)

    class Meta:
        model = TeacherTimeOff
        fields = [
            'id', 'teacher', 'start_date', 'end_date', 'reason',
            'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']


class TeacherReviewSerializer(serializers.ModelSerializer):
    """Serializer for Teacher Reviews."""

    student = UserSerializer(read_only=True)
    average_category_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = TeacherReview
        fields = [
            'id', 'teacher', 'student', 'session', 'overall_rating',
            'teaching_quality', 'communication', 'punctuality', 'patience',
            'review_text', 'pros', 'cons', 'is_approved', 'teacher_response',
            'response_date', 'is_verified_purchase', 'helpful_count',
            'created_at', 'average_category_rating'
        ]
        read_only_fields = [
            'id', 'student', 'is_approved', 'is_verified_purchase',
            'helpful_count', 'created_at'
        ]

    def validate(self, attrs):
        # Ensure all ratings are between 1 and 5
        rating_fields = ['overall_rating', 'teaching_quality', 'communication', 'punctuality', 'patience']
        for field in rating_fields:
            if field in attrs and (attrs[field] < 1 or attrs[field] > 5):
                raise serializers.ValidationError({field: "Rating must be between 1 and 5."})
        return attrs


class TeacherCertificationSerializer(serializers.ModelSerializer):
    """Serializer for Teacher Certifications."""

    class Meta:
        model = TeacherCertification
        fields = [
            'id', 'certification_name', 'issuing_organization',
            'issue_date', 'expiry_date', 'credential_id', 'credential_url',
            'document', 'is_verified', 'verified_date', 'created_at'
        ]
        read_only_fields = ['id', 'is_verified', 'verified_date', 'created_at']


class TeacherApplicationSerializer(serializers.Serializer):
    """Serializer for teacher application."""

    # User information
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    country = serializers.CharField()

    # Teacher qualifications
    education = serializers.CharField()
    years_of_experience = serializers.IntegerField()
    specializations = serializers.ListField(child=serializers.CharField())
    teaching_styles = serializers.ListField(child=serializers.CharField())
    languages_spoken = serializers.ListField(child=serializers.CharField())
    can_teach_age_groups = serializers.ListField(child=serializers.CharField())

    # Bio
    bio = serializers.CharField()
    teaching_methodology = serializers.CharField(required=False, allow_blank=True)
    introduction_video = serializers.URLField(required=False, allow_blank=True)

    # Documents
    ijazah = serializers.BooleanField(default=False)
    ijazah_document = serializers.FileField(required=False, allow_null=True)
    id_document = serializers.FileField(required=True)

    def create(self, validated_data):
        from users.models import User

        # Create user
        user_data = {
            'email': validated_data['email'],
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'phone_number': validated_data['phone_number'],
            'country': validated_data['country'],
            'user_type': 'teacher',
        }
        user = User.objects.create_user(
            password=validated_data['password'],
            **user_data
        )

        # Create teacher profile
        teacher_profile = TeacherProfile.objects.create(
            user=user,
            education=validated_data['education'],
            years_of_experience=validated_data['years_of_experience'],
            specializations=validated_data['specializations'],
            teaching_styles=validated_data['teaching_styles'],
            languages_spoken=validated_data['languages_spoken'],
            can_teach_age_groups=validated_data['can_teach_age_groups'],
            bio=validated_data['bio'],
            teaching_methodology=validated_data.get('teaching_methodology', ''),
            introduction_video=validated_data.get('introduction_video', ''),
            ijazah=validated_data.get('ijazah', False),
            ijazah_document=validated_data.get('ijazah_document'),
            id_document=validated_data['id_document'],
            application_status='pending'
        )

        return teacher_profile
