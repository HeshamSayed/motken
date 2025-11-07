"""
Learning models for Motken platform.
Handles curriculum, progress tracking, and learning materials.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from teachers.models import TeacherProfile
import uuid


class Curriculum(models.Model):
    """Learning curriculum/courses."""

    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    CURRICULUM_TYPE_CHOICES = (
        ('reading', 'Quran Reading'),
        ('tajweed', 'Tajweed Rules'),
        ('memorization', 'Quran Memorization'),
        ('understanding', 'Quran Understanding & Tafseer'),
        ('recitation', 'Beautiful Recitation'),
        ('arabic', 'Arabic Language'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    curriculum_type = models.CharField(max_length=30, choices=CURRICULUM_TYPE_CHOICES)

    # Details
    description = models.TextField()
    objectives = models.TextField(help_text="Learning objectives")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)

    # Prerequisites
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='unlocks')

    # Duration
    estimated_duration_weeks = models.IntegerField(help_text="Estimated completion time in weeks")
    total_lessons = models.IntegerField(default=0)

    # Thumbnail
    thumbnail = models.ImageField(upload_to='curricula/thumbnails/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='curricula/covers/', null=True, blank=True)

    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    # Age Groups
    min_age = models.IntegerField(null=True, blank=True)
    max_age = models.IntegerField(null=True, blank=True)

    # Enrollment
    enrolled_students = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'curricula'
        verbose_name = 'Curriculum'
        verbose_name_plural = 'Curricula'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Individual lessons within a curriculum."""

    LESSON_TYPE_CHOICES = (
        ('video', 'Video Lesson'),
        ('reading', 'Reading Material'),
        ('practice', 'Practice Exercise'),
        ('quiz', 'Quiz'),
        ('live', 'Live Session'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='lessons')

    title = models.CharField(max_length=200)
    slug = models.SlugField()
    lesson_number = models.IntegerField()

    # Content
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES)
    description = models.TextField()
    content = models.TextField(blank=True)

    # Duration
    estimated_duration_minutes = models.IntegerField(help_text="Estimated time to complete")

    # Resources
    video_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)
    pdf_file = models.FileField(upload_to='lessons/pdfs/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='lessons/thumbnails/', null=True, blank=True)

    # Quran References
    surah = models.CharField(max_length=100, blank=True)
    ayah_from = models.IntegerField(null=True, blank=True)
    ayah_to = models.IntegerField(null=True, blank=True)

    # Requirements
    requires_teacher = models.BooleanField(default=False, help_text="Requires live session with teacher")
    is_free = models.BooleanField(default=False, help_text="Free preview lesson")

    # Status
    is_published = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessons'
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['curriculum', 'lesson_number']
        unique_together = ['curriculum', 'lesson_number']

    def __str__(self):
        return f"{self.curriculum.name} - Lesson {self.lesson_number}: {self.title}"


class StudentProgress(models.Model):
    """Track student progress through curricula and lessons."""

    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_progress')
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='student_progress')

    # Progress
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    current_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_students')
    completed_lessons = models.ManyToManyField(Lesson, blank=True, related_name='completed_by')

    # Stats
    lessons_completed = models.IntegerField(default=0)
    lessons_total = models.IntegerField(default=0)
    progress_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Time
    total_time_spent_minutes = models.IntegerField(default=0)

    # Dates
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(null=True, blank=True)

    # Performance
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quiz_scores = models.JSONField(default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_progress'
        verbose_name = 'Student Progress'
        verbose_name_plural = 'Student Progress'
        unique_together = ['student', 'curriculum']
        indexes = [
            models.Index(fields=['student', 'status']),
        ]

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.curriculum.name} ({self.progress_percent}%)"

    def update_progress(self):
        """Recalculate progress percentage."""
        if self.lessons_total > 0:
            self.progress_percent = (self.lessons_completed / self.lessons_total) * 100
            if self.progress_percent >= 100:
                self.status = 'completed'
            elif self.progress_percent > 0:
                self.status = 'in_progress'
        self.save()


class LessonCompletion(models.Model):
    """Track completion of individual lessons."""

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_completions')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='completions')

    # Completion Details
    completed = models.BooleanField(default=False)
    time_spent_minutes = models.IntegerField(default=0)
    completion_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Score (for quizzes/assessments)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Notes
    student_notes = models.TextField(blank=True)

    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lesson_completions'
        verbose_name = 'Lesson Completion'
        verbose_name_plural = 'Lesson Completions'
        unique_together = ['student', 'lesson']
        indexes = [
            models.Index(fields=['student', 'completed']),
        ]

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.lesson.title}"


class Homework(models.Model):
    """Homework assignments."""

    STATUS_CHOICES = (
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('completed', 'Completed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_assignments')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='homework_assigned')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)

    # Assignment
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()

    # Surah/Ayah to practice
    surah = models.CharField(max_length=100, blank=True)
    ayah_from = models.IntegerField(null=True, blank=True)
    ayah_to = models.IntegerField(null=True, blank=True)

    # Deadlines
    assigned_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')

    # Submission
    submission_text = models.TextField(blank=True)
    submission_file = models.FileField(upload_to='homework/submissions/', null=True, blank=True)
    submission_audio = models.FileField(upload_to='homework/audio/', null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    # Review
    teacher_feedback = models.TextField(blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    reviewed_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'homework'
        verbose_name = 'Homework'
        verbose_name_plural = 'Homework'
        ordering = ['-due_date']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['teacher', 'status']),
        ]

    def __str__(self):
        return f"{self.title} - {self.student.get_full_name()}"

    @property
    def is_overdue(self):
        """Check if homework is overdue."""
        from django.utils import timezone
        return self.due_date < timezone.now() and self.status not in ['submitted', 'reviewed', 'completed']


class LearningMaterial(models.Model):
    """Downloadable learning materials and resources."""

    MATERIAL_TYPE_CHOICES = (
        ('pdf', 'PDF Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('document', 'Document'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)

    # File
    file = models.FileField(upload_to='learning_materials/')
    file_size = models.IntegerField(help_text="File size in bytes")
    thumbnail = models.ImageField(upload_to='materials/thumbnails/', null=True, blank=True)

    # Associated with
    curriculum = models.ForeignKey(Curriculum, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')

    # Access
    is_free = models.BooleanField(default=False)
    requires_subscription = models.BooleanField(default=True)

    # Stats
    download_count = models.IntegerField(default=0)

    # Status
    is_published = models.BooleanField(default=True)

    # Timestamps
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'learning_materials'
        verbose_name = 'Learning Material'
        verbose_name_plural = 'Learning Materials'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Achievement(models.Model):
    """Student achievements and badges."""

    ACHIEVEMENT_TYPE_CHOICES = (
        ('milestone', 'Milestone'),
        ('streak', 'Streak'),
        ('completion', 'Completion'),
        ('excellence', 'Excellence'),
        ('participation', 'Participation'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPE_CHOICES)

    # Badge
    badge_icon = models.ImageField(upload_to='achievements/badges/')
    badge_color = models.CharField(max_length=7, help_text="Hex color code")

    # Criteria
    criteria = models.JSONField(help_text="Achievement criteria")
    points = models.IntegerField(default=0, help_text="Points awarded")

    # Status
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'achievements'
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'

    def __str__(self):
        return self.name


class StudentAchievement(models.Model):
    """Track achievements earned by students."""

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    earned_at = models.DateTimeField(auto_now_add=True)
    is_notified = models.BooleanField(default=False)

    class Meta:
        db_table = 'student_achievements'
        verbose_name = 'Student Achievement'
        verbose_name_plural = 'Student Achievements'
        unique_together = ['student', 'achievement']
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.achievement.name}"
