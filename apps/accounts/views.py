from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers import (
    UserRegistrationSerializer,
)


class RegistrationAPIView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request: "Request", *args, **kwargs) -> "Response":
        """Post method that handles user registration from api endpoint"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(TokenObtainPairView):
    pass
