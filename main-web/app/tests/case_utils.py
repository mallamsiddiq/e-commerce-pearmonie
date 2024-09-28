# test_mixins.py
from unittest.mock import patch
from django.core.cache import cache

class EmptyCacheMixin:

    # @classmethod
    def tearDown(self):
        super().tearDown()
        self.clear_cache()

    
    def clear_cache(self):
        cache.clear()