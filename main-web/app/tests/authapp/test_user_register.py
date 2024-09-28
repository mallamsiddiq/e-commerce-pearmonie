# test_authentication.py
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class UserRegistrationTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('authapp:authentication-register')
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword123'
        }

    def test_successful_registration(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = get_user_model().objects.filter(email=self.valid_data['email']).first()
        self.assertIsNotNone(user)
        
        self.assertEqual(user.first_name, self.valid_data['first_name'])
        self.assertEqual(user.last_name, self.valid_data['last_name'])

    def test_registration_missing_password(self):
        data = self.valid_data.copy()
        data.pop('password')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('password', response.data['errors'][0]['attr'])
        self.assertEqual('required', response.data['errors'][0]['code'])
        
    def test_registration_invalid_email(self):
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('email', response.data['errors'][0]['attr'])
        self.assertEqual('invalid', response.data['errors'][0]['code'])
        
    def test_registration_duplicate_email(self):
        get_user_model().objects.create_user(**self.valid_data)
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('email', response.data['errors'][0]['attr'])
        self.assertEqual('unique', response.data['errors'][0]['code'])


