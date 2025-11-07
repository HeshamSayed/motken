"""
URLs for Learning app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CurriculumViewSet, LessonViewSet, StudentProgressViewSet,
    LessonCompletionViewSet, HomeworkViewSet, LearningMaterialViewSet,
    AchievementViewSet, StudentAchievementViewSet
)

app_name = 'learning'

router = DefaultRouter()
router.register(r'curricula', CurriculumViewSet, basename='curriculum')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'progress', StudentProgressViewSet, basename='student-progress')
router.register(r'completions', LessonCompletionViewSet, basename='lesson-completion')
router.register(r'homework', HomeworkViewSet, basename='homework')
router.register(r'materials', LearningMaterialViewSet, basename='learning-material')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'student-achievements', StudentAchievementViewSet, basename='student-achievement')

urlpatterns = [
    path('', include(router.urls)),
]
