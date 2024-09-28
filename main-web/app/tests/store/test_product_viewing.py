from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Product  # Ensure you have the correct import for your Product model
from django.contrib.auth import get_user_model
from tests.case_utils import EmptyCacheMixin


User = get_user_model()


class ProductViewSetTests(EmptyCacheMixin, APITestCase):


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
            'price':'100',
            'quantity':0
            
        }
        
        # Create products for users
        self.product1 = Product.objects.create(
            name='Product 1', store = self.store1, **self.product_payload)
        self.product2 = Product.objects.create(
            name='Product 2', store = self.store2, **((self.product_payload | {'price':'50',})))
        
        self.detail_url = reverse('store:products-detail', kwargs={'pk': self.product1.pk})
        self.list_url = reverse('store:products-list')
        self.popular_url = reverse('store:products-most-popular')
        
        self.client.force_authenticate(user=self.user1)


    def test_product_list(self):
        """Ensure that users can view all products."""
        

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming both users have one product
        self.assertEqual(response.data['results'][0]['name'], self.product2.name)
        self.assertEqual(response.data['results'][1]['name'], self.product1.name)


    @patch('store.task.log_user_interaction_task.delay')
    def test_product_retrieve(self, mock_seed_task):
        """Ensure that a user can retrieve their product details."""
        

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)
        
         # Check that it was called with the correct arguments
        product_instance = self.product1  # Get the last created product
        mock_seed_task.assert_called_with(str(self.user1.id), str(product_instance.id), product_instance.category)
        
    
    @patch('store.serializers.get_latest_currency_rate')
    @patch('store.serializers.validate_currency_from_api')
    @patch('store.task.log_user_interaction_task.delay')
    def test_retrieve_with_currency_conversion(self, mock_task, 
                                               mock_validate_currency, 
                                               mock_conversion):
        # Set up the mock return values
        mock_conversion.return_value = 0.85  # Mock conversion rate USD to EUR
        mock_validate_currency.return_value = True  # Mock validation of the currency
        
        # Authenticate the user
        self.client.force_authenticate(user=self.user1)
        
        # Call the retrieve endpoint with ?currency=EUR
        url = f"{self.detail_url}?currency=EUR"
        response = self.client.get(url)

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assuming USD to EUR conversion (100 * 0.85)
        expected_price_in_eur = 100.00 * 0.85
        self.assertAlmostEqual(float(response.data['converted_price']), expected_price_in_eur, places=2)

        # Ensure the mock was called correctly
        mock_conversion.assert_called_once_with('EUR', base_currency='USD')
        mock_validate_currency.assert_called_once_with('EUR')
        
    @patch('store.serializers.get_latest_currency_rate')
    @patch('store.serializers.validate_currency_from_api')
    @patch('store.task.log_user_interaction_task.delay')
    def test_list_with_currency_conversion(self, mock_task, 
                                               mock_validate_currency, 
                                               mock_conversion):
        # Set up the mock return values
        mock_conversion.return_value = 0.88  # Mock conversion rate USD to GBP
        mock_validate_currency.return_value = True  # Assuming this function validates currency correctly
        
        mock_conversion.return_value = 0.88
        response = self.client.get(f"{self.list_url}?currency=GBP")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Convert the products' prices to GBP using the mock
        product_2_converted = 50.00 * 0.88  # USD to GBP
        product_1_converted = 100.00 * 0.88  # USD to GBP (example rate)

        # Check the response data
        self.assertAlmostEqual(response.data['results'][0]['converted_price'], product_2_converted, places=2)
        self.assertAlmostEqual(response.data['results'][1]['converted_price'], product_1_converted, places=2)

        # Ensure the mock was called with the correct arguments
        mock_conversion.assert_called_once_with('GBP', base_currency = 'USD')
        mock_validate_currency.assert_called_once_with('GBP')
        
    def test_product_list_most_popular(self):
        
        # make a product popular
        self.product1.views_count = 10
        self.product1.save()
        self.product1.refresh_from_db()

        response = self.client.get(self.popular_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that products are returned in order of popularity
        products = response.json()['results']
        # Extract popularity for assertions
        popularity_order = [product['views_count'] for product in products]
         # Assert that the order is correct highest first
        self.assertEqual(popularity_order, sorted(popularity_order, reverse=True)) 
        
        # Alternatively, assert specific order based on created products
        self.assertEqual(products[0]['name'], self.product1.name)  # Most popular
        self.assertEqual(products[1]['name'], self.product2.name)  # least popular

    def test_increment_views_method(self):
        # Call the increment_views method with a viewer
        views_count = self.product1.views_count
        self.product1.increment_views(viewer=self.user2)
        
        # Check that the views_count has incremented by 1
        self.product1.refresh_from_db()  # Refresh the instance from the database
        self.assertEqual(self.product1.views_count, views_count + 1)
        
        # Check that the viewer has been added
        self.assertIn(self.user2, self.product1.viewers.all())

