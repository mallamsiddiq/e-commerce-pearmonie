from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name", "email", 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required':True}
        }
        
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "email",)
        
        
class AdminRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name", "email", 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required':True}
        }
        
    def validate_email(self, value):
        """
        Check that the email domain is 'pearmonie.com'.
        """
        if not value.endswith('@pearmonie.com'):
            raise serializers.ValidationError(_(" Invalid domain grant .."))
        return value
        
    def create(self, validated_data):
        user = get_user_model().objects.create_superuser(**validated_data)
        return user


class AdminLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Check if the user is an admin (you can customize this logic later)
        # this is to be user created through data syncronization dont have access
        if not self.user.is_staff:  # Or replace with your custom check
            raise AuthenticationFailed(
                "You are not authorized to login in here", 
                code=status.HTTP_403_FORBIDDEN
            )
        
        return data