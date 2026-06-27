from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import SAFE_METHODS, BasePermission


from .models import *
from .serializers import *
# Create your views here.


class ProductPermission(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):

        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )



class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(ModelViewSet):

    permission_classes = [ProductPermission]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    filter_backends = [DjangoFilterBackend,SearchFilter]

    filterset_fields = [
        'category',
        'featured',
        'is_active'
    ]

    search_fields = [
        'name',
        'description'
    ]
