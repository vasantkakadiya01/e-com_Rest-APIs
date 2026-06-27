from rest_framework import serializers
from .models import *

class OredrItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"



class OrderSerializer(serializers.ModelSerializer):

    item = OredrItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
