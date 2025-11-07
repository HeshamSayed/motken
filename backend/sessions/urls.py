"""
URLs for Sessions app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SessionViewSet, SessionProgressViewSet, SessionAttachmentViewSet,
    SessionMessageViewSet, SessionRatingViewSet, BookingRequestViewSet
)

app_name = 'sessions'

router = DefaultRouter()
router.register(r'', SessionViewSet, basename='session')
router.register(r'progress', SessionProgressViewSet, basename='session-progress')
router.register(r'attachments', SessionAttachmentViewSet, basename='session-attachment')
router.register(r'messages', SessionMessageViewSet, basename='session-message')
router.register(r'ratings', SessionRatingViewSet, basename='session-rating')
router.register(r'booking-requests', BookingRequestViewSet, basename='booking-request')

urlpatterns = [
    path('', include(router.urls)),
]
