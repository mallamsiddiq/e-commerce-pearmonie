import decimal
import logging
from authapp.models import User
from rest_framework import serializers, exceptions
from .models import Store, Product
from common.utils import get_latest_currency_rate, validate_currency_from_api
from .models.enums import CurrencyEnum

logger = logging.getLogger(__name__)
DEFAULT_CURRENCY = 'USD'

def validate_currency_and_fetch_rate(currency: str):
    if not validate_currency_from_api(currency):
        raise exceptions.ValidationError(
            f"Invalid currency. Supported currencies are {', '.join(CurrencyEnum.values())}",
        )
    try:
        return decimal.Decimal(get_latest_currency_rate(currency, base_currency=DEFAULT_CURRENCY))
    except Exception as e:
        logger.error(f"Error fetching conversion rate for {currency}: {e}")
        # fail silently 
        return decimal.Decimal(1)
    
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'owner']
        read_only_fields = ['owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class BaseProductSerializer(serializers.ModelSerializer):
    converted_price = serializers.SerializerMethodField()
    store_id = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(), required=False, 
        allow_null=True, write_only=True
    )
    owner = serializers.StringRelatedField(read_only = True, 
                                           source = 'store.owner',
                                           default = ''
    )

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['store']  # Store is set automatically

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_rate = self.set_conversion_rate()

    def set_conversion_rate(self):
        request = self.context.get('request')
        user_currency = request.query_params.get('currency', DEFAULT_CURRENCY).upper()

        if user_currency != DEFAULT_CURRENCY:
            return validate_currency_and_fetch_rate(user_currency)
        return decimal.Decimal(1)
    
    def get_converted_price(self, obj):
        return round(obj.price * self.conversion_rate, 2)
    

class ProductSerializer(BaseProductSerializer):
    store_id = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(), required=False, 
        allow_null=True, write_only=True
    )

    class Meta:
        model = Product
        exclude = ['viewers']
        read_only_fields = ['store']  # Store is set automatically
        
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        store = validated_data.pop('store_id', None)
        user: User = self.context['request'].user

        # If a store is provided, check ownership
        if store:
            if not (store.owner == user or user.is_superuser):
                raise exceptions.PermissionDenied(
                    "Only store owners or Admins can add product to store."
                )
            validated_data['store'] = store  # Set the valid store
        
        # If no store is provided and user has no default store: like superuser
        elif not (default_store:=user.stores.first()):
            raise exceptions.ValidationError(
                "No store available for this user. Admins must provide a store explicitly."
            )
        
        # If no store is provided, set the user's default store
        else:
            validated_data['store'] = default_store

        return validated_data

class ProductDetailSerializer(BaseProductSerializer):
    
    class Meta:
        model = Product
        exclude = ['viewers']
        read_only_fields = ['store'] 