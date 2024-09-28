from rest_framework.routers import DefaultRouter
from django.urls import path, include
from authapp.views import AuthViewSet, ProfileViewSet
app_name = 'authapp'

router = DefaultRouter()
router.register('auth', AuthViewSet, basename='authentication')
router.register('users', ProfileViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
]
