from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

class ProfileViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            first_name='testuser',
            password='testpassword',
            email='testuser@example.com'
        )
        
        self.user2 = get_user_model().objects.create_user(
            first_name='testuser 2',
            password='testpassword',
            email='testuser2@example.com'
        )

        self.admin_user = get_user_model().objects.create_superuser(
            first_name='adminuser',
            password='adminpassword',
            email='adminuser@example.com'
        )
        
        self.client.force_authenticate(user=self.user1)

    def test_user_can_only_access_their_personal_profile(self):
        url = reverse('authapp:users-me')
        response = self.client.get(url)

        # Ensure the response only contains the authenticated user's data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user1.first_name)

    def test_public_profile_is_open(self):
        # Authenticate as admin
        url = reverse('authapp:users-list')  # Use the correct URL for listing users
        response = self.client.get(url)

        # Ensure the admin can see all users
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()['results']), 2)  # Admin should see more than one user

        url = reverse('authapp:users-detail', kwargs={'pk': self.user2.pk})
         
        response = self.client.get(url)

        # Ensure the admin can see all users
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], str(self.user2.id))  # Admin should see more than one user

    def test_user_update_own_profile(self):
        url = reverse('authapp:users-update-me')  # User detail endpoint
        data = {'email': 'newemail@example.com'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()  # Refresh the user instance from the database
        self.assertEqual(self.user1.email, 'newemail@example.com')

    def test_admin_update_any_profile(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('authapp:users-detail', kwargs={'pk': self.user2.pk}) # User detail endpoint
        data = {'email': 'adminupdate@example.com'}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user2.refresh_from_db()  # Refresh the user instance from the database
        self.assertEqual(self.user2.email, 'adminupdate@example.com')
        
    def test_user_update_other_user_profile(self):
        # Authenticate as admin
        url = reverse('authapp:users-detail', kwargs={'pk': self.user2.pk}) # User detail endpoint
        data = {'email': 'hackupdate@example.com'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)