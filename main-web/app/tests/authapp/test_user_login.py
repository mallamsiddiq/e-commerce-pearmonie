from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model



class AdminUserLoginTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('authapp:authentication-login')
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword123'
        }
        
        get_user_model().objects.create_user(**self.user_data)
        
    def test_successful_login(self):
        response = self.client.post(self.url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_login_invalid_credentials(self):
        response = self.client.post(self.url, {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(self.url, {
            'email': 'wrongemail',
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
