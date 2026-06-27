from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from products.models import Product
from .serializers import *
# Create your views here.

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")

        quantity = request.data.get("quantity",1)

        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            item.quantity = int(quantity)
        else:
            item.quantity += int(quantity)

        item.save()

        return Response({
            "message":"Added to Cart"
        })

class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity"))

        cart = Cart.objects.get(user=request.user)

        item = CartItem.objects.get(
            cart=cart,
            product_id=product_id
        )

        item = CartItem.objects.first()
        item.quantity = quantity
        item.save()

        print(request.data)

        return Response({
            "message": "updated",
            "quantity": item.quantity
        })


class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart)

        serializer = CartItemSerializer(items, many=True)

        return Response(serializer.data)

class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        CartItem.objects.filter(id=item_id,cart__user=request.user).delete()

        return Response({"message":"Removed"})


class AddToWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        wishlist = Wishlist.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)

        WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)

        return Response({
             "message":"Added To Wishlist"
        })

class ViewWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        wishlist = Wishlist.objects.get(user=request.user)
        
        items = WishlistItem.objects.filter(wishlist=wishlist)

        serializer = WishlistItemSerializer(items, many=True)

        return Response(serializer.data)