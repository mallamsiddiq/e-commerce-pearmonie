from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Product  # Ensure you have the correct import for your Product model
from django.contrib.auth import get_user_model
from tests.case_utils import EmptyCacheMixin

User = get_user_model()

class ProductCreateSetTests(EmptyCacheMixin, APITestCase):


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
    
    
    @patch('store.task.seed_product_catalogue_task.delay')
    def test_product_create(self, mock_seed_task):
        """Ensure that authenticated users can create a product."""
        self.client.force_authenticate(user=self.user1)
        data = {'name': 'New Product'} | self.product_payload

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.filter(store=self.store1).count(), 2)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(Product.objects.first().name, 'New Product')
        
        # Check that it was called with the correct arguments
        product_instance = Product.objects.first()  # Get the last created product
        mock_seed_task.assert_called_with(product_instance.name, str(product_instance.id), product_instance.category)

    def test_create_product_as_non_store_owner(self):
        """Ensure that an admin can delete any product."""
        self.client.force_authenticate(user=self.user2)

        data = {'name': 'New Product', 'store_id':str(self.store1.pk)} | self.product_payload

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 2) #no addition 
        
    
    @patch('store.task.seed_product_catalogue_task.delay')
    def test_admin_can_create_product_on_any_store(self, mock_seed_task):
        """Ensure that an admin can delete any product."""
        self.client.force_authenticate(user=self.admin_user)

        data = {'name': 'New Product', 'store_id':str(self.store1.pk)} | self.product_payload

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.filter(store=self.store1).count(), 2)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(Product.objects.first().name, 'New Product')
        
        # Check that it was called with the correct arguments
        product_instance = Product.objects.first()  # Get the last created product
        mock_seed_task.assert_called_with(product_instance.name, str(product_instance.id), product_instance.category)

