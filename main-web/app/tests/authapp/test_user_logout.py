from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from django.core.cache import cache

User = get_user_model()

class LogoutTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.url = reverse('authapp:authentication-logout')
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@g.com', password='testpassword')
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = self.refresh.access_token

    def test_logout_success(self):
          # Ensure this matches your URL name for the logout view
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        response = self.client.post(self.url)
        
        # Assert the token is blacklisted
        self.assertTrue(cache.get(f"blacklisted_token_{self.access_token}"))

        # Assert the response status and message
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Successfully logged out.")
        
        # Assert user can access protected route with logged out token
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        
    def test_logout_without_authentication(self):
        
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

