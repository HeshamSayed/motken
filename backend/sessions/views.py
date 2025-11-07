"""
Session views and API endpoints.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta, datetime

from .models import (
    Session, SessionProgress, SessionAttachment, SessionMessage,
    SessionRating, BookingRequest
)
from .serializers import (
    SessionSerializer, SessionBookingSerializer, SessionProgressSerializer,
    SessionAttachmentSerializer, SessionMessageSerializer, SessionRatingSerializer,
    BookingRequestSerializer
)
from teachers.models import TeacherProfile
from users.models import StudentProfile


class SessionViewSet(viewsets.ModelViewSet):
    """Session ViewSet."""

    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'teacher', 'student']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Session.objects.all()
        elif user.user_type == 'teacher':
            return Session.objects.filter(teacher__user=user)
        else:
            return Session.objects.filter(student=user)

    @action(detail=False, methods=['post'])
    def book(self, request):
        """Book a new session."""
        serializer = SessionBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        teacher = serializer.validated_data['teacher_obj']

        # Calculate pricing
        duration = serializer.validated_data['duration']
        if duration == 30:
            session_price = float(teacher.session_30min_rate)
        elif duration == 45:
            session_price = float(teacher.session_45min_rate)
        else:
            session_price = float(teacher.session_60min_rate)

        # Apply trial discount
        if serializer.validated_data.get('is_trial'):
            session_price = session_price * 0.5  # 50% off for trial

        # Calculate fees (20% platform fee)
        platform_fee = session_price * 0.20
        teacher_payout = session_price - platform_fee

        # Create session
        session = Session.objects.create(
            student=request.user,
            teacher=teacher,
            scheduled_date=serializer.validated_data['scheduled_date'],
            scheduled_time=serializer.validated_data['scheduled_time'],
            duration=duration,
            curriculum=serializer.validated_data.get('curriculum', ''),
            lesson_topic=serializer.validated_data.get('lesson_topic', ''),
            session_goals=serializer.validated_data.get('session_goals', ''),
            session_price=session_price,
            teacher_payout=teacher_payout,
            platform_fee=platform_fee,
            is_trial=serializer.validated_data.get('is_trial', False),
            status='scheduled'
        )

        # TODO: Create Zoom meeting
        # TODO: Send notifications

        return Response({
            'message': 'Session booked successfully',
            'session': SessionSerializer(session).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def my_sessions(self, request):
        """Get current user's sessions."""
        sessions = self.get_queryset().order_by('-scheduled_date', '-scheduled_time')

        page = self.paginate_queryset(sessions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a session."""
        session = self.get_object()

        if not session.can_cancel:
            return Response({
                'error': 'Session cannot be cancelled less than 24 hours before scheduled time'
            }, status=status.HTTP_400_BAD_REQUEST)

        cancellation_reason = request.data.get('cancellation_reason', '')

        if request.user == session.student:
            session.status = 'cancelled_by_student'
        elif request.user == session.teacher.user:
            session.status = 'cancelled_by_teacher'
        else:
            return Response({
                'error': 'You are not authorized to cancel this session'
            }, status=status.HTTP_403_FORBIDDEN)

        session.cancellation_reason = cancellation_reason
        session.cancelled_at = timezone.now()
        session.cancelled_by = request.user
        session.save()

        # TODO: Process refund if applicable
        # TODO: Send notifications

        return Response({
            'message': 'Session cancelled successfully',
            'session': SessionSerializer(session).data
        })

    @action(detail=True, methods=['get'])
    def join(self, request, pk=None):
        """Get Zoom join URL for session."""
        session = self.get_object()

        if session.status != 'scheduled':
            return Response({
                'error': 'Session is not scheduled'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if session is within 15 minutes of start time
        session_datetime = timezone.make_aware(
            datetime.combine(session.scheduled_date, session.scheduled_time)
        )
        now = timezone.now()

        if now < session_datetime - timedelta(minutes=15):
            return Response({
                'error': 'Session cannot be joined more than 15 minutes before start time'
            }, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Generate/retrieve Zoom meeting URL

        return Response({
            'zoom_join_url': session.zoom_join_url or 'https://zoom.us/j/placeholder',
            'zoom_meeting_password': session.zoom_meeting_password,
            'session': SessionSerializer(session).data
        })

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark session as completed."""
        session = self.get_object()

        # Only teacher can mark as completed
        if request.user != session.teacher.user:
            return Response({
                'error': 'Only teacher can mark session as completed'
            }, status=status.HTTP_403_FORBIDDEN)

        session.status = 'completed'
        session.actual_end_time = timezone.now()

        if session.actual_start_time:
            duration = (session.actual_end_time - session.actual_start_time).seconds // 60
            session.actual_duration = duration

        session.save()

        # Update statistics
        session.teacher.total_sessions_taught += 1
        session.teacher.save()

        student_profile = StudentProfile.objects.filter(user=session.student).first()
        if student_profile:
            student_profile.total_sessions_completed += 1
            student_profile.sessions_remaining -= 1
            student_profile.save()

        return Response({
            'message': 'Session marked as completed',
            'session': SessionSerializer(session).data
        })


class SessionProgressViewSet(viewsets.ModelViewSet):
    """Session Progress ViewSet."""

    queryset = SessionProgress.objects.all()
    serializer_class = SessionProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return SessionProgress.objects.all()
        elif user.user_type == 'teacher':
            return SessionProgress.objects.filter(session__teacher__user=user)
        else:
            return SessionProgress.objects.filter(session__student=user)


class SessionAttachmentViewSet(viewsets.ModelViewSet):
    """Session Attachment ViewSet."""

    queryset = SessionAttachment.objects.all()
    serializer_class = SessionAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class SessionMessageViewSet(viewsets.ModelViewSet):
    """Session Message ViewSet."""

    queryset = SessionMessage.objects.all()
    serializer_class = SessionMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'teacher':
            return SessionMessage.objects.filter(session__teacher__user=user)
        else:
            return SessionMessage.objects.filter(session__student=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class SessionRatingViewSet(viewsets.ModelViewSet):
    """Session Rating ViewSet."""

    queryset = SessionRating.objects.all()
    serializer_class = SessionRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class BookingRequestViewSet(viewsets.ModelViewSet):
    """Booking Request ViewSet."""

    queryset = BookingRequest.objects.all()
    serializer_class = BookingRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'teacher':
            return BookingRequest.objects.filter(teacher__user=user)
        else:
            return BookingRequest.objects.filter(student=user)

    def perform_create(self, serializer):
        teacher_id = self.request.data.get('teacher')
        teacher = TeacherProfile.objects.get(id=teacher_id)

        expires_at = timezone.now() + timedelta(hours=48)
        serializer.save(student=self.request.user, teacher=teacher, expires_at=expires_at)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept booking request."""
        booking_request = self.get_object()

        if request.user != booking_request.teacher.user:
            return Response({
                'error': 'Only teacher can accept this request'
            }, status=status.HTTP_403_FORBIDDEN)

        # Create session
        # Similar logic to book action above

        booking_request.status = 'accepted'
        booking_request.responded_at = timezone.now()
        booking_request.save()

        return Response({
            'message': 'Booking request accepted',
            'booking_request': BookingRequestSerializer(booking_request).data
        })

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject booking request."""
        booking_request = self.get_object()

        if request.user != booking_request.teacher.user:
            return Response({
                'error': 'Only teacher can reject this request'
            }, status=status.HTTP_403_FORBIDDEN)

        booking_request.status = 'rejected'
        booking_request.response_message = request.data.get('message', '')
        booking_request.responded_at = timezone.now()
        booking_request.save()

        return Response({
            'message': 'Booking request rejected',
            'booking_request': BookingRequestSerializer(booking_request).data
        })
