from .models import Payments, Orders, Products
from rest_framework.serializers import ModelSerializer
from user_auth.user_serializer import UserListingSerializer

class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields='__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['worker_user'] = UserListingSerializer(instance.worker_user).data if instance.worker_user else None
        return data
    
class OrdersSerializer(ModelSerializer):
    class Meta:
        model = Orders
        fields='__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['worker_user'] = UserListingSerializer(instance.worker_user).data if instance.worker_user else None
        data['customer_user'] = UserListingSerializer(instance.customer_user).data if instance.customer_user else None
        return data
    

    
class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields='__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['added_by'] = UserListingSerializer(instance.added_by).data if instance.added_by else None
        return data