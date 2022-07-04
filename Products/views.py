from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsOwnerOrReadOnly, IsSellerOrReadOnly
from Products.serializers import ProductCreateSerializer

from .models import Product


class ListCreateProductView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly, IsAuthenticatedOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class RetrieveUpdateProductView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
