"""
Tests for Sessions app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, time, timedelta
from decimal import Decimal

from teachers.models import TeacherProfile
from sessions.models import Session

User = get_user_model()


class SessionBookingTests(TestCase):
    """Test session booking functionality."""

    def setUp(self):
        self.client = APIClient()

        # Create student
        self.student = User.objects.create_user(
            email='student@test.com',
            password='TestPass123!',
            first_name='John',
            last_name='Doe',
            user_type='student'
        )

        # Create teacher
        self.teacher_user = User.objects.create_user(
            email='teacher@test.com',
            password='TestPass123!',
            first_name='Ahmed',
            last_name='Hassan',
            user_type='teacher'
        )
        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher_user,
            bio='Test teacher',
            years_of_experience=5,
            specializations=['tajweed'],
            education='BA',
            teaching_styles=['patient'],
            languages_spoken=['en'],
            can_teach_age_groups=['adults'],
            session_30min_rate=Decimal('15.00'),
            session_45min_rate=Decimal('20.00'),
            session_60min_rate=Decimal('25.00'),
            application_status='approved',
            is_available=True
        )

        self.client.force_authenticate(user=self.student)

    def test_book_session(self):
        """Test booking a session."""
        tomorrow = date.today() + timedelta(days=2)
        data = {
            'teacher': str(self.teacher_profile.id),
            'scheduled_date': tomorrow.isoformat(),
            'scheduled_time': '10:00:00',
            'duration': 30,
            'curriculum': 'Tajweed Basics',
            'lesson_topic': 'Noon Saakin'
        }

        response = self.client.post('/api/v1/sessions/book/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('session', response.data)

    def test_book_session_in_past(self):
        """Test booking session in the past fails."""
        yesterday = date.today() - timedelta(days=1)
        data = {
            'teacher': str(self.teacher_profile.id),
            'scheduled_date': yesterday.isoformat(),
            'scheduled_time': '10:00:00',
            'duration': 30
        }

        response = self.client.post('/api/v1/sessions/book/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_my_sessions(self):
        """Test getting user's sessions."""
        response = self.client.get('/api/v1/sessions/my_sessions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SessionCancellationTests(TestCase):
    """Test session cancellation."""

    def setUp(self):
        self.client = APIClient()

        self.student = User.objects.create_user(
            email='student@test.com',
            password='TestPass123!',
            first_name='John',
            last_name='Doe',
            user_type='student'
        )

        teacher_user = User.objects.create_user(
            email='teacher@test.com',
            password='TestPass123!',
            first_name='Ahmed',
            last_name='Hassan',
            user_type='teacher'
        )
        teacher_profile = TeacherProfile.objects.create(
            user=teacher_user,
            bio='Test',
            years_of_experience=5,
            specializations=['tajweed'],
            education='BA',
            teaching_styles=['patient'],
            languages_spoken=['en'],
            can_teach_age_groups=['adults'],
            application_status='approved'
        )

        # Create session scheduled 2 days from now
        future_date = date.today() + timedelta(days=2)
        self.session = Session.objects.create(
            student=self.student,
            teacher=teacher_profile,
            scheduled_date=future_date,
            scheduled_time=time(10, 0),
            duration=30,
            session_price=Decimal('15.00'),
            teacher_payout=Decimal('12.00'),
            platform_fee=Decimal('3.00'),
            status='scheduled'
        )

        self.client.force_authenticate(user=self.student)

    def test_cancel_session(self):
        """Test cancelling a session."""
        data = {'cancellation_reason': 'Emergency'}
        response = self.client.post(
            f'/api/v1/sessions/{self.session.id}/cancel/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.session.refresh_from_db()
        self.assertEqual(self.session.status, 'cancelled_by_student')
