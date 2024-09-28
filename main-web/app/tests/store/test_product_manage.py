from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Product  # Ensure you have the correct import for your Product model
from django.contrib.auth import get_user_model
from tests.case_utils import EmptyCacheMixin

User = get_user_model()

class ProductManageSetTests(EmptyCacheMixin, APITestCase):


    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(email='user1@n.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@n.com', password='password123')
        self.admin_user = User.objects.create_superuser(email='admin@n.com', password='password123')
        
        # A store is auto created for every non admin user
        self.store1 = self.user1.stores.first()
        self.store2 = self.user2.stores.first()
        
        self.product_payload = {
            'category':'cat 1',
            'description':'Description',
            'price':'50',
            'quantity':0
            
        }
        
        # Create products for users
        self.product1 = Product.objects.create(
            name='Product 1', store = self.store1, **self.product_payload)
        self.product2 = Product.objects.create(
            name='Product 2', store = self.store2, **self.product_payload)
        
        self.detail_url = reverse('store:products-detail', kwargs={'pk': self.product1.pk})
        self.list_url = reverse('store:products-list')
    
    def test_product_update_as_owner(self):
        """Ensure that the product owner can successfully update their product."""
        self.client.force_authenticate(user=self.user1)
        data = {'name': 'Updated Product Name'}

        response = self.client.patch(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Updated Product Name')

    def test_product_update_as_non_owner(self):
        """Ensure that a non-owner cannot update someone else's product."""
        self.client.force_authenticate(user=self.user2)
        data = {'name': 'Hacked Product Name'}

        response = self.client.patch(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.product1.refresh_from_db()
        self.assertNotEqual(self.product1.name, 'Hacked Product Name')

    def test_admin_can_update_any_product(self):
        """Ensure that an admin can update any product."""
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'Admin Changed Product Name'}

        response = self.client.patch(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Admin Changed Product Name')
        self.assertEqual(self.product1.store.owner, self.user1)  # Owner should remain unchanged

    def test_product_delete_as_owner(self):
        """Ensure that the product owner can successfully delete their product."""
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product1.pk).exists())

    def test_product_delete_as_non_owner(self):
        """Ensure that a non-owner cannot delete someone else's product."""
        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Product.objects.filter(pk=self.product1.pk).exists())

    def test_admin_can_delete_any_product(self):
        """Ensure that an admin can delete any product."""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product1.pk).exists())
        self.assertEqual(self.product1.store.owner, self.user1)  # Owner should remain unchanged
