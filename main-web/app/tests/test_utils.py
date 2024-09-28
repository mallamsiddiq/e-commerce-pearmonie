import unittest, requests
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.conf import settings
from django.core.cache import cache, caches
from common.utils import (
        convert_currency, get_latest_currency_rate, 
        validate_currency_from_api, blacklist_access_token, 
        is_access_token_blacklisted, cache_result, generate_cache_key)
from common.utils.recommendation_api import seed_product_catalogue, log_user_interaction
from store.task import seed_product_catalogue_task, log_user_interaction_task
from .case_utils import EmptyCacheMixin


class UtilsTestCase(EmptyCacheMixin, TestCase):

    # Currency conversion tests
    @patch('common.utils.currency.requests.get')
    def test_currency_conversion_success(self, mock_get):
        # Mock API response for successful currency conversion
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'data': {'USD': 1.0, 'EUR': 0.85}}
        
        result = convert_currency('EUR', 100, 'USD',)
        self.assertAlmostEqual(result, 85)

    @patch('common.utils.currency.requests.get')
    def test_currency_conversion_failure(self, mock_get):
        # Mock API response for failed currency conversion
        mock_get.return_value.status_code = 400
        mock_get.return_value.raise_for_status.side_effect = \
            requests.exceptions.HTTPError("API request failed")
        
        result = convert_currency('XYZ', 100, 'USD')
        self.assertEqual(result, 100, "Expected 100 no conversion fail silently")

    # Latest currency rate tests
    @patch('common.utils.currency.requests.get')
    def test_get_latest_currency_rate_success(self, mock_get):
        # Mock successful API call to get the latest currency rate
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'data': 
            {'EUR': 0.85}}
        
        result = get_latest_currency_rate('EUR')
        self.assertEqual(result, 0.85,)

    @patch('common.utils.currency.requests.get')
    def test_get_latest_currency_rate_failure(self, mock_get):
        # Mock API failure when fetching currency rate
        
        mock_get.return_value.status_code = 400
        mock_get.return_value.raise_for_status.side_effect = \
            requests.exceptions.HTTPError("API request failed")
        
        result = get_latest_currency_rate('EUR')
        self.assertEqual(result, 1, "Expected 1  no conversion fail silently")
        
    @patch('common.utils.currency.requests.get')
    def test_validate_currency_from_api_success(self, mock_get):
        # Mock successful API call to get the latest currency rate
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'data': 
            {'EUR': 0.85}}
        
        result = validate_currency_from_api('EUR')
        self.assertTrue(result)

    @patch('common.utils.currency.requests.get')
    def test_validate_currency_from_api_failure(self, mock_get):
        # Mock API failure when fetching currency rate
        
        mock_get.return_value.status_code = 400
        mock_get.return_value.raise_for_status.side_effect = \
            requests.exceptions.HTTPError("API request failed")
        
        result = validate_currency_from_api('EUR')
        self.assertFalse(result)

    # Product recommendation catalogue seeding tests
    @patch('common.utils.recommendation_api.requests.post')
    def test_seed_product_catalogue_success(self, mock_post):
        # Mock successful product catalogue seeding
        mock_post.return_value.status_code = 201
        # mock_post.return_value.json.return_value = True
        result = seed_product_catalogue('product_name_1', 'product_id_1', 'category_1')
        self.assertTrue(result, "Seeding product catalogue failed")

    @patch('common.utils.recommendation_api.requests.post')
    def test_seed_product_catalogue_failure(self, mock_post):
        # Mock failure in product catalogue seeding
        mock_post.return_value.status_code = 400
        mock_post.return_value.raise_for_status.side_effect = \
            requests.exceptions.HTTPError("API request failed")
        result = seed_product_catalogue('product_name_1', 'product_id_1', 'category_1')
        self.assertFalse(result, "Seeding product catalogue failed")

    # User interaction logging tests
    @patch('common.utils.recommendation_api.requests.post')
    def test_log_user_interaction_success(self, mock_post):
        # Mock successful logging of user interaction
        mock_post.return_value.status_code = 201
        
        result = log_user_interaction('user_id_1', 'product_id_1', 'category_1')
        self.assertTrue(result, "Logging user interaction failed")

    @patch('common.utils.recommendation_api.requests.post')
    def test_log_user_interaction_failure(self, mock_post):
        # Mock failure in logging user interaction
        mock_post.return_value.status_code = 500
        mock_post.return_value.raise_for_status.side_effect = \
            requests.exceptions.HTTPError("API request failed")
        
        result = log_user_interaction('user_id_1', 'product_id_1', 'category_1')
        self.assertFalse(result, "Expected logging user interaction to fail")

    # Background task for product catalogue seeding
    @patch('store.task.seed_product_catalogue')
    def test_seed_product_catalogue_task(self, mock_seed):
        # Simulate successful task execution
        mock_seed.return_value = None
        seed_product_catalogue_task('product_name', 'product_id_1', 'category_1')
        mock_seed.assert_called_once_with('product_name', 'product_id_1', 'category_1')

    # Background task for logging user interaction
    @patch('store.task.log_user_interaction')
    def test_log_user_interaction_task(self, mock_log):
        # Simulate successful task execution
        mock_log.return_value = None
        log_user_interaction_task('user_id_1', 'product_id_1', 'category_1')
        mock_log.assert_called_once_with('user_id_1', 'product_id_1', 'category_1')
        
    @patch('common.utils.cache.hashlib.md5')
    def test_generate_cache_key(self, mock_hash_key):
        expected_key = 'Ebfda47611a349d9428'
        
        mock_hash_key.return_value.hexdigest=lambda:expected_key
        def sample_function(arg1, arg2):
            return arg1 + arg2

        # Generate cache key
        generated_key = generate_cache_key(sample_function, 1, 2)
        
        # Check if the generated key is valid
        self.assertEqual(generated_key, expected_key)

    @patch('common.utils.cache.generate_cache_key')
    def test_cache_result_decorator(self, mock_key):
        # Mock the return value of generate_cache_key
        cache_key = 'generated_key'
        mock_key.return_value = cache_key
        
        @cache_result(timeout=120)
        def add(a, b):
            return a + b

        # First call should calculate the result
        first_result = add(3, 4)
        self.assertEqual(first_result, 7)

        # Second call should return cached result
        cached_result = add(3, 4)
        self.assertEqual(cached_result, 7)

        # Ensure it uses the cache by checking the cache directly
        self.assertEqual(cache.get(cache_key), 7)
        
    def test_blacklist_access_token(self):
        token = 'aacfda47611a349d9428'
        # Ensure the token is not blacklisted initially
        self.assertIsNone(cache.get(f"blacklisted_token_{token}"))
        
        # Blacklist the token
        blacklist_access_token(token)
        
         # Ensure the token is now blacklisted
        self.assertTrue(cache.get(f"blacklisted_token_{token}"))
        
        redis_cache_client = caches['default'].client.get_client()
        ttl = redis_cache_client.ttl(f"test_cache:1:blacklisted_token_{token}")
        
        access_token_lifetime = settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME")

        self.assertEqual(access_token_lifetime.total_seconds(), ttl)
       
    def test_is_access_token_blacklisted_non_blacklisted(self):
        # Check with a non-blacklisted token
        token = 'ddcfda47611a349d9428'
        self.assertFalse(is_access_token_blacklisted(token=token))
        cache.set(f"blacklisted_token_{token}", True, 10)
        self.assertTrue(is_access_token_blacklisted(token=token))
        