from rest_framework import generics
from .models import Product
from .serializers import ListProductSerialzier, CreateProductSerializer
from .permissions import MyCustomPermission,IsProductSeller
from rest_framework.authentication import TokenAuthentication
from.mixins import SerializerByMethodMixin


class ListCreateProductView(SerializerByMethodMixin,generics.ListCreateAPIView):
    permission_classes =[MyCustomPermission]
    queryset = Product.objects.all()
    serializer_map = {
        'GET':ListProductSerialzier,
        'POST':CreateProductSerializer
    }
    def perform_create(self,serializer):
        serializer.save(seller_id=self.request.user)

class RetriveUpdateProductView(SerializerByMethodMixin,generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProductSeller,MyCustomPermission]
    queryset = Product.objects.all()
    serializer_map = {
        'GET':ListProductSerialzier,
        'PATCH':CreateProductSerializer
    }