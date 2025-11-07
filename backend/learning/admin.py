"""
Admin configuration for Learning app.
"""

from django.contrib import admin
from .models import (
    Curriculum, Lesson, StudentProgress, LessonCompletion,
    Homework, LearningMaterial, Achievement, StudentAchievement
)


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    """Admin interface for Curricula."""

    list_display = ['name', 'curriculum_type', 'difficulty', 'total_lessons', 'enrolled_students', 'is_published']
    list_filter = ['curriculum_type', 'difficulty', 'is_published', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'enrolled_students', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'curriculum_type', 'difficulty')
        }),
        ('Content', {
            'fields': ('description', 'objectives')
        }),
        ('Duration', {
            'fields': ('estimated_duration_weeks', 'total_lessons')
        }),
        ('Prerequisites', {
            'fields': ('prerequisites',)
        }),
        ('Media', {
            'fields': ('thumbnail', 'cover_image')
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured', 'display_order')
        }),
        ('Age Groups', {
            'fields': ('min_age', 'max_age')
        }),
        ('Statistics', {
            'fields': ('enrolled_students',)
        }),
    )

    actions = ['publish_curricula', 'feature_curricula']

    def publish_curricula(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} curriculum/curricula published.')
    publish_curricula.short_description = 'Publish selected curricula'

    def feature_curricula(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} curriculum/curricula featured.')
    feature_curricula.short_description = 'Feature selected curricula'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin interface for Lessons."""

    list_display = ['title', 'curriculum', 'lesson_number', 'lesson_type', 'is_published', 'is_free']
    list_filter = ['lesson_type', 'is_published', 'is_free', 'requires_teacher']
    search_fields = ['title', 'description', 'curriculum__name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('curriculum', 'title', 'slug', 'lesson_number', 'lesson_type')
        }),
        ('Content', {
            'fields': ('description', 'content')
        }),
        ('Duration', {
            'fields': ('estimated_duration_minutes',)
        }),
        ('Resources', {
            'fields': ('video_url', 'audio_url', 'pdf_file', 'thumbnail')
        }),
        ('Quran References', {
            'fields': ('surah', 'ayah_from', 'ayah_to')
        }),
        ('Requirements', {
            'fields': ('requires_teacher', 'is_free')
        }),
        ('Status', {
            'fields': ('is_published',)
        }),
    )

    actions = ['publish_lessons']

    def publish_lessons(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} lesson(s) published.')
    publish_lessons.short_description = 'Publish selected lessons'


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    """Admin interface for Student Progress."""

    list_display = ['student', 'curriculum', 'status', 'progress_percent', 'lessons_completed', 'lessons_total']
    list_filter = ['status', 'curriculum']
    search_fields = ['student__email', 'student__first_name', 'curriculum__name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Student & Curriculum', {
            'fields': ('student', 'curriculum')
        }),
        ('Progress', {
            'fields': ('status', 'current_lesson', 'lessons_completed', 'lessons_total', 'progress_percent')
        }),
        ('Time', {
            'fields': ('total_time_spent_minutes', 'started_at', 'completed_at', 'last_accessed')
        }),
        ('Performance', {
            'fields': ('average_score', 'quiz_scores')
        }),
    )


@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    """Admin interface for Lesson Completions."""

    list_display = ['student', 'lesson', 'completed', 'completion_percentage', 'score']
    list_filter = ['completed', 'lesson__curriculum']
    search_fields = ['student__email', 'lesson__title']
    readonly_fields = ['last_accessed']


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    """Admin interface for Homework."""

    list_display = ['title', 'student', 'teacher', 'status', 'due_date', 'score']
    list_filter = ['status', 'assigned_date', 'due_date']
    search_fields = ['title', 'student__email', 'teacher__user__email']
    readonly_fields = ['id', 'assigned_date', 'created_at', 'updated_at']
    date_hierarchy = 'due_date'

    fieldsets = (
        ('Assignment Details', {
            'fields': ('student', 'teacher', 'lesson', 'title', 'description', 'instructions')
        }),
        ('Quran References', {
            'fields': ('surah', 'ayah_from', 'ayah_to')
        }),
        ('Deadlines & Status', {
            'fields': ('assigned_date', 'due_date', 'status')
        }),
        ('Submission', {
            'fields': ('submission_text', 'submission_file', 'submission_audio', 'submitted_at')
        }),
        ('Review', {
            'fields': ('teacher_feedback', 'score', 'reviewed_at')
        }),
    )

    actions = ['mark_reviewed']

    def mark_reviewed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='reviewed', reviewed_at=timezone.now())
        self.message_user(request, f'{updated} homework assignment(s) marked as reviewed.')
    mark_reviewed.short_description = 'Mark selected homework as reviewed'


@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    """Admin interface for Learning Materials."""

    list_display = ['title', 'material_type', 'curriculum', 'lesson', 'is_free', 'download_count']
    list_filter = ['material_type', 'is_free', 'is_published', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'download_count', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'material_type')
        }),
        ('File', {
            'fields': ('file', 'file_size', 'thumbnail')
        }),
        ('Association', {
            'fields': ('curriculum', 'lesson')
        }),
        ('Access', {
            'fields': ('is_free', 'requires_subscription', 'is_published')
        }),
        ('Statistics', {
            'fields': ('download_count',)
        }),
        ('Uploader', {
            'fields': ('uploaded_by',)
        }),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Admin interface for Achievements."""

    list_display = ['name', 'achievement_type', 'points', 'is_active']
    list_filter = ['achievement_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'achievement_type')
        }),
        ('Badge', {
            'fields': ('badge_icon', 'badge_color')
        }),
        ('Criteria & Points', {
            'fields': ('criteria', 'points')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(StudentAchievement)
class StudentAchievementAdmin(admin.ModelAdmin):
    """Admin interface for Student Achievements."""

    list_display = ['student', 'achievement', 'earned_at', 'is_notified']
    list_filter = ['is_notified', 'earned_at']
    search_fields = ['student__email', 'achievement__name']
    readonly_fields = ['earned_at']
