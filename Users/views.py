from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView, Response, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAdmin

from .permissions import IsAccountOwnerOrReadOnly
from Users.serializer import (
    AccountSerializer,
    AccountManagementSerializer,
    LoginSerializer,
)
from .models import User


class ListNewestUserView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        max_users = self.kwargs["amount_users"]
        return self.queryset.order_by("id")[0:max_users]


class ListCreateUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class UpdateUserView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAccountOwnerOrReadOnly]

    queryset = User.objects.all()
    serializer_class = AccountSerializer


class UpdateManagementView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    queryset = User.objects.all()
    serializer_class = AccountManagementSerializer


class LoginUsersView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"token": token.key})

        return Response(
            {"message": "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED
        )
