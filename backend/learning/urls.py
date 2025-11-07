"""
URLs for Learning app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'learning'

# Placeholder for viewsets - to be implemented
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]
