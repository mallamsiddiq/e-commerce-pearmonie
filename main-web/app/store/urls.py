from rest_framework.routers import DefaultRouter
from django.urls import path, include
from store.views import ProductViewSet, StoreViewSet
app_name = 'store'

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('', StoreViewSet, basename='stores')

urlpatterns = [
    path('store/', include(router.urls)),
]
