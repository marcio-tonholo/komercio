from rest_framework import serializers
from .models import Product
from users.serializers import UserSerializers

class CreateProductSerializer(serializers.ModelSerializer):
    seller= UserSerializers(read_only=True,source='seller_id')
    class Meta:
        model=Product
        fields = ['id','description','price','quantity','is_active',"seller"]
        extra_kwargs = {'quantity':{'min_value':0}}

class ListProductSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['description','price','quantity','is_active','seller_id']