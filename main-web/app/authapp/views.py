from django.contrib.auth import get_user_model
from rest_framework import (status, viewsets, permissions)
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from drf_spectacular.utils import extend_schema
from authapp.serializers import (
    RegistrationSerializer, UserSerializer, 
    AdminRegistrationSerializer
)

from common.utils import blacklist_access_token


class AuthViewSet(viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in {'retrieve', 'destroy', 'list'}:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], url_path='register', 
            permission_classes=[permissions.AllowAny],
            serializer_class=RegistrationSerializer)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = self.serializer_class(user).data
        return Response({'detail': 'User registered successfully', **user_data}, 
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='login',
            permission_classes=[permissions.AllowAny],
            serializer_class=TokenObtainPairView.serializer_class)
    def login(self, request):
        view = TokenObtainPairView.as_view()
        return view(request._request)
    
    @action(detail=False, methods=['post'], url_path='refresh-blacklist',
            permission_classes=[permissions.AllowAny], 
            serializer_class = TokenBlacklistView)
    def refresh_blacklist(self, request):
        view = TokenBlacklistView.as_view()
        return view(request._request)
    
    @action(detail=False, methods=['post'], url_path='logout',
            permission_classes=[permissions.IsAuthenticated],)
    def logout(self, request):
        access_token = request.auth
        blacklist_access_token(access_token)
        return Response({"message": "Successfully logged out."}, status=200)


    @extend_schema(
        summary="Register a new Admin user",
        description="Only emails with a @pearmonie domain are allowed to register here."
    )
    @action(detail=False, methods=['post'], url_path='admin-signup', 
            url_name='admin-signup', permission_classes=[permissions.AllowAny],
            serializer_class=AdminRegistrationSerializer)
    def admin_signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = self.serializer_class(user).data
        return Response({'detail': 'Admin registered successfully', **user_data}, 
                        status=status.HTTP_201_CREATED)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in {'update', 'destroy', 'partial_update'}:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def my_profile(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], url_name='update-me', url_path='update-me')
    def my_profile_update(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Save the updated user data
        return Response(serializer.data)