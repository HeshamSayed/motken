"""
URLs for Teachers app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TeacherProfileViewSet, TeacherAvailabilityViewSet, TeacherTimeOffViewSet,
    TeacherReviewViewSet, TeacherCertificationViewSet
)

app_name = 'teachers'

router = DefaultRouter()
router.register(r'profiles', TeacherProfileViewSet, basename='teacher-profile')
router.register(r'availability', TeacherAvailabilityViewSet, basename='teacher-availability')
router.register(r'time-off', TeacherTimeOffViewSet, basename='teacher-time-off')
router.register(r'reviews', TeacherReviewViewSet, basename='teacher-review')
router.register(r'certifications', TeacherCertificationViewSet, basename='teacher-certification')

urlpatterns = [
    path('', include(router.urls)),
]
