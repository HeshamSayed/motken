"""
Teacher views and API endpoints.
"""

from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import (
    TeacherProfile, TeacherAvailability, TeacherTimeOff,
    TeacherReview, TeacherCertification
)
from .serializers import (
    TeacherProfileSerializer, TeacherListSerializer, TeacherAvailabilitySerializer,
    TeacherTimeOffSerializer, TeacherReviewSerializer, TeacherCertificationSerializer,
    TeacherApplicationSerializer
)


class IsTeacherOrReadOnly(permissions.BasePermission):
    """Custom permission for teachers."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.user_type == 'teacher'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class TeacherProfileViewSet(viewsets.ModelViewSet):
    """Teacher Profile ViewSet."""

    queryset = TeacherProfile.objects.filter(application_status='approved')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specializations', 'is_available', 'is_featured']
    search_fields = ['user__first_name', 'user__last_name', 'bio', 'specializations']
    ordering_fields = ['average_rating', 'years_of_experience', 'session_30min_rate']
    ordering = ['-average_rating']

    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherListSerializer
        return TeacherProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)

        # Filter by max price
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(session_30min_rate__lte=max_price)

        # Filter by experience
        min_experience = self.request.query_params.get('min_experience')
        if min_experience:
            queryset = queryset.filter(years_of_experience__gte=min_experience)

        return queryset

    @action(detail=False, methods=['post'])
    def apply(self, request):
        """Apply to become a teacher."""
        serializer = TeacherApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher_profile = serializer.save()

        return Response({
            'message': 'Application submitted successfully',
            'teacher_profile': TeacherProfileSerializer(teacher_profile).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current teacher's profile."""
        if request.user.user_type != 'teacher':
            return Response({
                'error': 'You are not a teacher'
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            profile = TeacherProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except TeacherProfile.DoesNotExist:
            return Response({
                'error': 'Teacher profile not found'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get teacher reviews."""
        teacher = self.get_object()
        reviews = TeacherReview.objects.filter(
            teacher=teacher,
            is_approved=True
        ).order_by('-created_at')

        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = TeacherReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TeacherReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get teacher availability."""
        teacher = self.get_object()
        availability = TeacherAvailability.objects.filter(
            teacher=teacher,
            is_active=True
        )
        serializer = TeacherAvailabilitySerializer(availability, many=True)
        return Response(serializer.data)


class TeacherAvailabilityViewSet(viewsets.ModelViewSet):
    """Teacher Availability ViewSet."""

    queryset = TeacherAvailability.objects.all()
    serializer_class = TeacherAvailabilitySerializer
    permission_classes = [IsTeacherOrReadOnly]

    def get_queryset(self):
        if self.request.user.user_type == 'teacher':
            return TeacherAvailability.objects.filter(teacher__user=self.request.user)
        return TeacherAvailability.objects.filter(is_active=True)

    def perform_create(self, serializer):
        teacher_profile = TeacherProfile.objects.get(user=self.request.user)
        serializer.save(teacher=teacher_profile)


class TeacherTimeOffViewSet(viewsets.ModelViewSet):
    """Teacher Time Off ViewSet."""

    queryset = TeacherTimeOff.objects.all()
    serializer_class = TeacherTimeOffSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def get_queryset(self):
        if self.request.user.user_type == 'teacher':
            return TeacherTimeOff.objects.filter(teacher__user=self.request.user)
        return TeacherTimeOff.objects.none()

    def perform_create(self, serializer):
        teacher_profile = TeacherProfile.objects.get(user=self.request.user)
        serializer.save(teacher=teacher_profile)


class TeacherReviewViewSet(viewsets.ModelViewSet):
    """Teacher Review ViewSet."""

    queryset = TeacherReview.objects.filter(is_approved=True)
    serializer_class = TeacherReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['teacher', 'overall_rating']
    ordering_fields = ['created_at', 'overall_rating', 'helpful_count']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['post'])
    def helpful(self, request, pk=None):
        """Mark review as helpful."""
        review = self.get_object()
        review.helpful_count += 1
        review.save()

        return Response({
            'message': 'Review marked as helpful',
            'helpful_count': review.helpful_count
        })

    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """Teacher responds to review."""
        review = self.get_object()

        # Check if user is the teacher
        if review.teacher.user != request.user:
            return Response({
                'error': 'You can only respond to your own reviews'
            }, status=status.HTTP_403_FORBIDDEN)

        response_text = request.data.get('response')
        if not response_text:
            return Response({
                'error': 'Response text is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        review.teacher_response = response_text
        review.response_date = timezone.now()
        review.save()

        return Response({
            'message': 'Response added successfully',
            'review': TeacherReviewSerializer(review).data
        })


class TeacherCertificationViewSet(viewsets.ModelViewSet):
    """Teacher Certification ViewSet."""

    queryset = TeacherCertification.objects.all()
    serializer_class = TeacherCertificationSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def get_queryset(self):
        if self.request.user.user_type == 'teacher':
            return TeacherCertification.objects.filter(teacher__user=self.request.user)
        # Only show verified certifications to non-teachers
        return TeacherCertification.objects.filter(is_verified=True)

    def perform_create(self, serializer):
        teacher_profile = TeacherProfile.objects.get(user=self.request.user)
        serializer.save(teacher=teacher_profile)
