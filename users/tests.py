from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import UserProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_register_post_valid(self):
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_register_post_invalid(self):
        data = {
            'email': 'invalid-email',
            'username': '',
            'password1': 'pass',
            'password2': 'different'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='invalid-email').exists())


class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_post_valid(self):
        data = {
            'username': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)

    def test_login_post_invalid(self):
        data = {
            'username': 'test@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('profile')
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.login(email='test@example.com', password='testpass123')

    def test_profile_get_authenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomUserChangeForm)

    def test_profile_get_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)

    def test_profile_update_valid(self):
        data = {
            'update_profile': '',
            'email': 'updated@example.com',
            'username': 'updateduser',
            'phone_number': '9876543210',
            'date_of_birth': '1985-05-15'
        }
        response = self.client.post(self.profile_url, data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_password_update_valid(self):
        data = {
            'update_password': '',
            'old_password': 'testpass123',
            'new_password1': 'newpass123',
            'new_password2': 'newpass123'
        }
        response = self.client.post(self.profile_url, data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('password was successfully updated' in str(m) for m in messages))
