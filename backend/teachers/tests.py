"""
Tests for Teachers app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from teachers.models import TeacherProfile, TeacherReview

User = get_user_model()


class TeacherProfileTests(TestCase):
    """Test teacher profile functionality."""

    def setUp(self):
        self.client = APIClient()
        self.teacher_user = User.objects.create_user(
            email='teacher@test.com',
            password='TestPass123!',
            first_name='Ahmed',
            last_name='Hassan',
            user_type='teacher'
        )
        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher_user,
            bio='Experienced Quran teacher',
            years_of_experience=10,
            specializations=['tajweed', 'memorization'],
            education='Bachelor in Islamic Studies',
            teaching_styles=['patient'],
            languages_spoken=['ar', 'en'],
            can_teach_age_groups=['adults', 'children'],
            session_30min_rate=15.00,
            session_45min_rate=20.00,
            session_60min_rate=25.00,
            application_status='approved'
        )

    def test_list_teachers(self):
        """Test listing approved teachers."""
        response = self.client.get('/api/v1/teachers/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_get_teacher_detail(self):
        """Test getting teacher detail."""
        response = self.client.get(f'/api/v1/teachers/profiles/{self.teacher_profile.id}/')
        self.assertEqual(response.status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], 'teacher@test.com')

    def test_filter_teachers_by_specialization(self):
        """Test filtering teachers by specialization."""
        response = self.client.get('/api/v1/teachers/profiles/?specializations=tajweed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeacherReviewTests(TestCase):
    """Test teacher review functionality."""

    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create_user(
            email='student@test.com',
            password='TestPass123!',
            first_name='John',
            last_name='Doe',
            user_type='student'
        )
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
            application_status='approved'
        )
        self.client.force_authenticate(user=self.student)

    def test_create_review(self):
        """Test creating a teacher review."""
        data = {
            'teacher': str(self.teacher_profile.id),
            'overall_rating': 5,
            'teaching_quality': 5,
            'communication': 5,
            'punctuality': 5,
            'patience': 5,
            'review_text': 'Excellent teacher!'
        }
        response = self.client.post('/api/v1/teachers/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_rating(self):
        """Test creating review with invalid rating."""
        data = {
            'teacher': str(self.teacher_profile.id),
            'overall_rating': 6,  # Invalid
            'teaching_quality': 5,
            'communication': 5,
            'punctuality': 5,
            'patience': 5,
            'review_text': 'Test'
        }
        response = self.client.post('/api/v1/teachers/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
