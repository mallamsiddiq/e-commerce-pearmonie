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
            raise serializers.ValidationError(_(" Invalid domain grant .. only  @pearmonie.com)"))
        return value
        
    def create(self, validated_data):
        user = get_user_model().objects.create_superuser(**validated_data)
        return user