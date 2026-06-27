from rest_framework import serializers
from .models import *
from products.models import *
from products.serializers import *

class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = "__all__"

class WishlistItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = "__all__"