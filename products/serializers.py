from rest_framework import serializers
from .models import Product
from users.serializers import UserSerializers

class CreateProductSerializer(serializers.ModelSerializer):
    seller_id = UserSerializers(read_only=True)
    class Meta:
        model=Product
        fields = ['id','description','price','quantity','is_active','seller_id']
        extra_kwargs = {'seller_id':{'read_only':True}}

class ListProductSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['description','price','quantity','is_active','seller_id']