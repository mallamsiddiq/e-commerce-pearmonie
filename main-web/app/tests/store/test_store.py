from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Store
from django.contrib.auth import get_user_model
from tests.case_utils import EmptyCacheMixin

User = get_user_model()

class StoreViewSetTests(EmptyCacheMixin, APITestCase):
    
    

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(email='user1@n.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@n.com', password='password123')
        self.admin_user = User.objects.create_superuser(email='admin@n.com', password='password123')

        # A store is auto created for every non admin user
        self.store1 = self.user1.stores.first()
        self.store2 = self.user2.stores.first()
        
        self.detail_url = reverse('store:stores-detail', kwargs={'pk': self.store1.pk})
        self.list_url = reverse('store:stores-list')


    def test_store_create(self):
        """
        Ensure that authenticated users can create a store.
        """
        from django.core.cache import cache
        
        self.client.force_authenticate(user=self.user1)
          # Assuming your viewset is named 'store-list'
          
        data = {'name': 'New Store'}
        response = self.client.post(self.list_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Store.objects.filter(owner = self.user1).count(), 2)  # One already exists, one new is created
        self.assertEqual(Store.objects.first().name, 'New Store')
        self.assertEqual(Store.objects.first().owner, self.user1)

    def test_store_list(self):
        """
        Ensure that users can view all stores.
        """
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # user1 has only 1 store
        self.assertEqual(response.data['results'][0]['name'], 'user2 Store')
        self.assertEqual(response.data['results'][1]['name'], 'user1 Store')

    def test_store_retrieve(self):
        """
        Ensure that a user can retrieve their store details.
        """
        self.client.force_authenticate(user=self.user1)
        

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'user1 Store')
        
    def test_store_update_as_owner(self):
        """
        Ensure that the store owner can successfully update their store.
        """
        self.client.force_authenticate(user=self.user1)

        data = {'name': 'Updated Store Name'}
        response = self.client.put(self.detail_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.store1.refresh_from_db()  # Reload the store from the database
        self.assertEqual(self.store1.name, 'Updated Store Name')

    def test_store_update_as_non_owner(self):
        """
        Ensure that a non-owner cannot update someone else's store.
        """
        self.client.force_authenticate(user=self.user2)

        data = {'name': 'Hacked Store Name'}
        response = self.client.put(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # User2 shouldn't find the store

        self.store1.refresh_from_db()
        self.assertNotEqual(self.store1.name, 'Hacked Store Name')

    def test_admin_can_update_any_store(self):
        """
        Ensure that a non-owner cannot update someone else's store.
        """
        self.client.force_authenticate(user=self.admin_user)

        data = {'name': 'Admin Changed Store Name'}
        response = self.client.put(self.detail_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # User2 shouldn't find the store

        self.store1.refresh_from_db()
        self.assertEqual(self.store1.name, 'Admin Changed Store Name')
        # assert admin is not the owner
        self.assertNotEqual(self.store1.owner, self.admin_user)
        self.assertEqual(self.store1.owner, self.user1)
        
    def test_store_delete_as_owner(self):
        """
        Ensure that the store owner can successfully delete their store.
        """
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # 204 No Content expected on successful delete
        self.assertFalse(Store.objects.filter(pk=self.store1.pk).exists())  # Store should no longer exist

    def test_store_delete_as_non_owner(self):
        """
        Ensure that a non-owner cannot delete someone else's store.
        """
        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Non-owner should get 404
        self.assertTrue(Store.objects.filter(pk=self.store1.pk).exists())  # Store should still exist

    def test_admin_can_delete_any_sore(self):
        """
        Ensure that unauthenticated users cannot delete any store.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # 204 No Content expected on successful delete
        self.assertFalse(Store.objects.filter(pk=self.store1.pk).exists())  # Store should no longer exist
        
        # assert admin is not the owner
        self.assertNotEqual(self.store1.owner, self.admin_user)
        self.assertEqual(self.store1.owner, self.user1)