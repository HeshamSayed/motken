"""
URLs for Users app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'users'

# Placeholder for viewsets - to be implemented
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # JWT endpoints will be added here
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
