"""
Learning serializers for API.
"""

from rest_framework import serializers
from .models import (
    Curriculum, Lesson, StudentProgress, LessonCompletion,
    Homework, LearningMaterial, Achievement, StudentAchievement
)
from users.serializers import UserSerializer


class CurriculumSerializer(serializers.ModelSerializer):
    """Serializer for Curriculum."""

    class Meta:
        model = Curriculum
        fields = [
            'id', 'name', 'slug', 'curriculum_type', 'description', 'objectives',
            'difficulty', 'estimated_duration_weeks', 'total_lessons', 'thumbnail',
            'cover_image', 'is_published', 'is_featured', 'display_order',
            'min_age', 'max_age', 'enrolled_students', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'enrolled_students', 'created_at', 'updated_at']


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson."""

    class Meta:
        model = Lesson
        fields = [
            'id', 'curriculum', 'title', 'slug', 'lesson_number', 'lesson_type',
            'description', 'content', 'estimated_duration_minutes', 'video_url',
            'audio_url', 'pdf_file', 'thumbnail', 'surah', 'ayah_from', 'ayah_to',
            'requires_teacher', 'is_free', 'is_published', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LessonListSerializer(serializers.ModelSerializer):
    """Simplified serializer for lesson list."""

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'lesson_number', 'lesson_type',
            'estimated_duration_minutes', 'is_free', 'requires_teacher'
        ]


class StudentProgressSerializer(serializers.ModelSerializer):
    """Serializer for Student Progress."""

    curriculum = CurriculumSerializer(read_only=True)
    current_lesson = LessonListSerializer(read_only=True)

    class Meta:
        model = StudentProgress
        fields = [
            'id', 'student', 'curriculum', 'status', 'current_lesson',
            'lessons_completed', 'lessons_total', 'progress_percent',
            'total_time_spent_minutes', 'average_score', 'quiz_scores',
            'started_at', 'completed_at', 'last_accessed', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'lessons_completed', 'progress_percent', 'started_at',
            'completed_at', 'created_at', 'updated_at'
        ]


class LessonCompletionSerializer(serializers.ModelSerializer):
    """Serializer for Lesson Completion."""

    lesson = LessonListSerializer(read_only=True)

    class Meta:
        model = LessonCompletion
        fields = [
            'id', 'student', 'lesson', 'completed', 'time_spent_minutes',
            'completion_percentage', 'score', 'max_score', 'student_notes',
            'started_at', 'completed_at', 'last_accessed'
        ]
        read_only_fields = ['id', 'started_at', 'completed_at', 'last_accessed']


class HomeworkSerializer(serializers.ModelSerializer):
    """Serializer for Homework."""

    from teachers.serializers import TeacherListSerializer
    teacher = TeacherListSerializer(read_only=True)
    lesson = LessonListSerializer(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Homework
        fields = [
            'id', 'student', 'teacher', 'lesson', 'title', 'description',
            'instructions', 'surah', 'ayah_from', 'ayah_to', 'assigned_date',
            'due_date', 'status', 'submission_text', 'submission_file',
            'submission_audio', 'submitted_at', 'teacher_feedback', 'score',
            'reviewed_at', 'created_at', 'updated_at', 'is_overdue'
        ]
        read_only_fields = [
            'id', 'assigned_date', 'status', 'teacher_feedback', 'score',
            'reviewed_at', 'created_at', 'updated_at'
        ]


class HomeworkSubmissionSerializer(serializers.Serializer):
    """Serializer for homework submission."""

    submission_text = serializers.CharField(required=False, allow_blank=True)
    submission_file = serializers.FileField(required=False, allow_null=True)
    submission_audio = serializers.FileField(required=False, allow_null=True)


class LearningMaterialSerializer(serializers.ModelSerializer):
    """Serializer for Learning Material."""

    curriculum = CurriculumSerializer(read_only=True)
    lesson = LessonListSerializer(read_only=True)
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = LearningMaterial
        fields = [
            'id', 'title', 'description', 'material_type', 'file', 'file_size',
            'thumbnail', 'curriculum', 'lesson', 'is_free', 'requires_subscription',
            'download_count', 'is_published', 'uploaded_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'download_count', 'uploaded_by', 'created_at', 'updated_at']


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement."""

    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'achievement_type', 'badge_icon',
            'badge_color', 'criteria', 'points', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class StudentAchievementSerializer(serializers.ModelSerializer):
    """Serializer for Student Achievement."""

    achievement = AchievementSerializer(read_only=True)
    student = UserSerializer(read_only=True)

    class Meta:
        model = StudentAchievement
        fields = [
            'id', 'student', 'achievement', 'earned_at', 'is_notified'
        ]
        read_only_fields = ['id', 'student', 'earned_at']
