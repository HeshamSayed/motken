"""
Learning views and API endpoints.
"""

from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import (
    Curriculum, Lesson, StudentProgress, LessonCompletion,
    Homework, LearningMaterial, Achievement, StudentAchievement
)
from .serializers import (
    CurriculumSerializer, LessonSerializer, LessonListSerializer,
    StudentProgressSerializer, LessonCompletionSerializer,
    HomeworkSerializer, HomeworkSubmissionSerializer,
    LearningMaterialSerializer, AchievementSerializer,
    StudentAchievementSerializer
)


class CurriculumViewSet(viewsets.ReadOnlyModelViewSet):
    """Curriculum ViewSet."""

    queryset = Curriculum.objects.filter(is_published=True)
    serializer_class = CurriculumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['curriculum_type', 'difficulty', 'is_featured']
    search_fields = ['name', 'description', 'objectives']
    ordering_fields = ['enrolled_students', 'created_at', 'display_order']
    ordering = ['display_order']

    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        """Get lessons for a curriculum."""
        curriculum = self.get_object()
        lessons = Lesson.objects.filter(
            curriculum=curriculum,
            is_published=True
        ).order_by('lesson_number')

        page = self.paginate_queryset(lessons)
        if page is not None:
            serializer = LessonSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll in a curriculum."""
        curriculum = self.get_object()

        # Check if already enrolled
        progress, created = StudentProgress.objects.get_or_create(
            student=request.user,
            curriculum=curriculum,
            defaults={
                'lessons_total': curriculum.total_lessons,
                'started_at': timezone.now()
            }
        )

        if created:
            curriculum.enrolled_students += 1
            curriculum.save()

        return Response({
            'message': 'Enrolled successfully' if created else 'Already enrolled',
            'progress': StudentProgressSerializer(progress).data
        }, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """Lesson ViewSet."""

    queryset = Lesson.objects.filter(is_published=True)
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['curriculum', 'lesson_type', 'is_free']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by curriculum if provided
        curriculum_id = self.request.query_params.get('curriculum')
        if curriculum_id:
            queryset = queryset.filter(curriculum_id=curriculum_id)

        return queryset.order_by('lesson_number')

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark lesson as completed."""
        lesson = self.get_object()

        # Get or create lesson completion
        completion, created = LessonCompletion.objects.get_or_create(
            student=request.user,
            lesson=lesson,
            defaults={'started_at': timezone.now()}
        )

        # Update completion data
        time_spent = request.data.get('time_spent_minutes', 0)
        score = request.data.get('score')
        notes = request.data.get('notes', '')

        completion.time_spent_minutes = time_spent
        completion.completed = True
        completion.completion_percentage = 100
        completion.completed_at = timezone.now()
        completion.student_notes = notes

        if score is not None:
            completion.score = score

        completion.save()

        # Update student progress
        try:
            progress = StudentProgress.objects.get(
                student=request.user,
                curriculum=lesson.curriculum
            )
            if lesson not in progress.completed_lessons.all():
                progress.completed_lessons.add(lesson)
                progress.lessons_completed += 1
                progress.total_time_spent_minutes += time_spent
                progress.update_progress()
        except StudentProgress.DoesNotExist:
            pass

        return Response({
            'message': 'Lesson completed',
            'completion': LessonCompletionSerializer(completion).data
        })


class StudentProgressViewSet(viewsets.ModelViewSet):
    """Student Progress ViewSet."""

    queryset = StudentProgress.objects.all()
    serializer_class = StudentProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['curriculum', 'status']

    def get_queryset(self):
        if self.request.user.is_staff:
            return StudentProgress.objects.all()
        return StudentProgress.objects.filter(student=self.request.user)

    @action(detail=False, methods=['get'])
    def my_progress(self, request):
        """Get current user's progress across all curricula."""
        progress = self.get_queryset().order_by('-last_accessed')

        page = self.paginate_queryset(progress)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)


class LessonCompletionViewSet(viewsets.ModelViewSet):
    """Lesson Completion ViewSet."""

    queryset = LessonCompletion.objects.all()
    serializer_class = LessonCompletionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return LessonCompletion.objects.all()
        return LessonCompletion.objects.filter(student=self.request.user)


class HomeworkViewSet(viewsets.ModelViewSet):
    """Homework ViewSet."""

    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'teacher', 'lesson']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['due_date']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Homework.objects.all()
        elif user.user_type == 'teacher':
            return Homework.objects.filter(teacher__user=user)
        else:
            return Homework.objects.filter(student=user)

    @action(detail=False, methods=['get'])
    def my_homework(self, request):
        """Get current student's homework."""
        homework = self.get_queryset().order_by('-due_date')

        page = self.paginate_queryset(homework)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(homework, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit homework."""
        homework = self.get_object()

        if request.user != homework.student:
            return Response({
                'error': 'You can only submit your own homework'
            }, status=status.HTTP_403_FORBIDDEN)

        if homework.status == 'submitted':
            return Response({
                'error': 'Homework already submitted'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = HomeworkSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        homework.submission_text = serializer.validated_data.get('submission_text', '')
        homework.submission_file = serializer.validated_data.get('submission_file')
        homework.submission_audio = serializer.validated_data.get('submission_audio')
        homework.status = 'submitted'
        homework.submitted_at = timezone.now()
        homework.save()

        return Response({
            'message': 'Homework submitted successfully',
            'homework': HomeworkSerializer(homework).data
        })

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Teacher reviews homework."""
        homework = self.get_object()

        if request.user != homework.teacher.user:
            return Response({
                'error': 'Only the assigned teacher can review this homework'
            }, status=status.HTTP_403_FORBIDDEN)

        feedback = request.data.get('feedback')
        score = request.data.get('score')

        if not feedback:
            return Response({
                'error': 'Feedback is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        homework.teacher_feedback = feedback
        if score is not None:
            homework.score = score
        homework.status = 'reviewed'
        homework.reviewed_at = timezone.now()
        homework.save()

        return Response({
            'message': 'Homework reviewed successfully',
            'homework': HomeworkSerializer(homework).data
        })


class LearningMaterialViewSet(viewsets.ModelViewSet):
    """Learning Material ViewSet."""

    queryset = LearningMaterial.objects.filter(is_published=True)
    serializer_class = LearningMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['material_type', 'curriculum', 'lesson', 'is_free']
    search_fields = ['title', 'description']

    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Track material download."""
        material = self.get_object()
        material.download_count += 1
        material.save()

        return Response({
            'message': 'Download tracked',
            'file_url': material.file.url if material.file else None
        })


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """Achievement ViewSet."""

    queryset = Achievement.objects.filter(is_active=True)
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StudentAchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """Student Achievement ViewSet."""

    queryset = StudentAchievement.objects.all()
    serializer_class = StudentAchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return StudentAchievement.objects.all()
        return StudentAchievement.objects.filter(student=self.request.user)

    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """Get current user's achievements."""
        achievements = self.get_queryset().order_by('-earned_at')

        page = self.paginate_queryset(achievements)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(achievements, many=True)
        return Response(serializer.data)
