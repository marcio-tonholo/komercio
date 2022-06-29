from rest_framework import serializers
from .models import User


class UserSerializers (serializers.ModelSerializer):
    class Meta:
        model=User
        fields =["id","email","first_name","last_name","is_seller","date_joined","password","is_active"]
        extra_kwargs = {"password":{"write_only":True},"is_active":{"read_only":True} }

    def create(self, validated_data):
        user =User.objects.create_user(**validated_data)
        return user

    
class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields =["id","email","first_name","last_name","is_seller","date_joined","is_active"]
        read_only_fields = ["id","email","first_name","last_name","is_seller","date_joined"]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()