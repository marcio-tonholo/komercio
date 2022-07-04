from rest_framework import generics
from .models import User
from .serializers import UserSerializers,LoginSerializer,ManagementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .permissions import IsAccountOwner,MyCustomPermission

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class UserUpdateView(generics.UpdateAPIView):
    permission_classes =[IsAccountOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializers

class UserManagementView(generics.UpdateAPIView):
    permission_classes =[MyCustomPermission]
    queryset = User.objects.all()
    serializer_class = ManagementSerializer

class NewestUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    def get_queryset(self):
        max_users = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:max_users]    

class LoginView(APIView):
    def post(self, request):
      serializer = LoginSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
      
      if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
      
      return Response(
              {"detail": "invalid email or password"},
              status=status.HTTP_401_UNAUTHORIZED,
            )
