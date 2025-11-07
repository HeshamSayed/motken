"""
User serializers for authentication and profile management.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, StudentProfile, DeviceToken, UserActivity


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'user_type',
            'phone_number', 'date_of_birth', 'gender', 'profile_picture',
            'country', 'timezone', 'preferred_language', 'is_active',
            'is_verified', 'email_verified', 'phone_verified',
            'biometric_enabled', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'is_verified', 'email_verified', 'phone_verified', 'date_joined', 'last_login']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'user_type', 'phone_number', 'date_of_birth', 'gender',
            'country', 'preferred_language', 'parent_email'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Check parental consent for minors
        if attrs.get('date_of_birth'):
            from datetime import date
            today = date.today()
            age = today.year - attrs['date_of_birth'].year - (
                (today.month, today.day) < (attrs['date_of_birth'].month, attrs['date_of_birth'].day)
            )
            if age < 18 and not attrs.get('parent_email'):
                raise serializers.ValidationError({"parent_email": "Parent email is required for users under 18."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        # Check if requires parental consent
        if validated_data.get('date_of_birth'):
            from datetime import date
            today = date.today()
            age = today.year - validated_data['date_of_birth'].year
            if age < 18:
                validated_data['requires_parental_consent'] = True

        user = User.objects.create_user(password=password, **validated_data)

        # Create student profile if user is a student
        if user.user_type == 'student':
            StudentProfile.objects.create(user=user)

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer."""

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom claims
        data['user'] = UserSerializer(self.user).data

        # Log activity
        UserActivity.objects.create(
            user=self.user,
            action='login',
            ip_address=self.context.get('request').META.get('REMOTE_ADDR'),
            user_agent=self.context.get('request').META.get('HTTP_USER_AGENT', '')
        )

        return data


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for Student Profile."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'user', 'learning_goals', 'current_skill_level',
            'preferred_teacher_gender', 'preferred_session_duration',
            'preferred_days', 'preferred_times', 'total_sessions_completed',
            'total_hours_learned', 'current_curriculum', 'current_lesson',
            'current_package', 'sessions_remaining', 'subscription_active',
            'subscription_expires_at', 'average_rating', 'total_ratings', 'notes'
        ]
        read_only_fields = [
            'total_sessions_completed', 'total_hours_learned',
            'average_rating', 'total_ratings'
        ]


class DeviceTokenSerializer(serializers.ModelSerializer):
    """Serializer for Device Token."""

    class Meta:
        model = DeviceToken
        fields = ['id', 'token', 'platform', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for User Activity."""

    class Meta:
        model = UserActivity
        fields = ['action', 'ip_address', 'timestamp', 'metadata']
        read_only_fields = fields
