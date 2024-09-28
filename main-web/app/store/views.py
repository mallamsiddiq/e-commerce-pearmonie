from django.shortcuts import render

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from store.models import Store, Product
from store.serializers import StoreSerializer, ProductSerializer, ProductDetailSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.select_related('owner').all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Admins can view all stores
        if self.request.user.is_staff or self.action in {'list', 'retrieve'}:
            return Store.objects.all()
        return Store.objects.filter(owner=self.request.user)  # Users manage only their own stores

    # @method_decorator(cache_page(60 * 60 * .5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('store__owner').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in {'retrieve', 'partial_update', 'update'}:
            return ProductDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.is_staff or self.action in {'list', 'retrieve', 'most_popular'}: # Admins can manage all products
            return super().get_queryset()
        return super().get_queryset().filter(store__owner=self.request.user)  # Users manage only products from their own stores
    
    
    @method_decorator(cache_page(60 * 5, key_prefix='products_'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='most-popular')
    @method_decorator(cache_page(60 * 5, key_prefix='popular_products'))
    def most_popular(self, request, *args, **kwargs):
        self.queryset =  super().get_queryset().order_by('-views_count')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        product.increment_views(request.user)
        
        return super().retrieve(request, *args, **kwargs)

        