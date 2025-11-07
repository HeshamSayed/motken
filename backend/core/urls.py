"""
URL configuration for Motken project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # API Endpoints
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/teachers/', include('teachers.urls')),
    path('api/v1/sessions/', include('sessions.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/learning/', include('learning.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = 'Motken Administration'
admin.site.site_title = 'Motken Admin'
admin.site.index_title = 'Welcome to Motken Administration'
