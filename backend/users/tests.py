"""
Tests for Users app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserRegistrationTests(TestCase):
    """Test user registration."""

    def setUp(self):
        self.client = APIClient()

    def test_register_student(self):
        """Test registering a student user."""
        data = {
            'email': 'student@test.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': 'student',
            'phone_number': '+1234567890',
            'country': 'USA',
            'preferred_language': 'en'
        }

        response = self.client.post('/api/v1/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)

    def test_register_with_mismatched_passwords(self):
        """Test registration with mismatched passwords."""
        data = {
            'email': 'test@test.com',
            'password': 'TestPass123!',
            'password_confirm': 'DifferentPass123!',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': 'student'
        }

        response = self.client.post('/api/v1/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAuthenticationTests(TestCase):
    """Test user authentication."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@test.com',
            password='TestPass123!',
            first_name='John',
            last_name='Doe'
        )

    def test_user_login(self):
        """Test user login."""
        data = {
            'email': 'test@test.com',
            'password': 'TestPass123!'
        }

        response = self.client.post('/api/v1/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'email': 'test@test.com',
            'password': 'WrongPassword'
        }

        response = self.client.post('/api/v1/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTests(TestCase):
    """Test user profile management."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@test.com',
            password='TestPass123!',
            first_name='John',
            last_name='Doe'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_profile(self):
        """Test retrieving user profile."""
        response = self.client.get('/api/v1/auth/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@test.com')

    def test_update_user_profile(self):
        """Test updating user profile."""
        data = {
            'first_name': 'Jane',
            'country': 'Canada'
        }

        response = self.client.patch('/api/v1/auth/users/update_profile/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Jane')
