from django.shortcuts import render
from accounts.permissions import IsAdminRole
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import razorpay
from rest_framework.permissions import IsAdminUser

from cart.models import *
from .models import *
from .serializers import *
from django.conf import settings
# Create your views here.


class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"error":"Cart is empty"})


        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response({
                    "error":f"{item.product.name} is out of stock"
                })

        total = 0

        for item in cart_items:
            total +=(item.product.price * item.quantity)

        order = Order.objects.create(user=request.user,total_amount=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

        return Response({
            "message":"Order Placed Successfully",
            "order_id":order.id
        })


class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-id")

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):

        order = Order.objects.get(id=order_id, user = request.user)
        serializer = OrderSerializer(order)

        return Response(serializer.data)

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):

        order = Order.objects.get(id=order_id, user = request.user)

        if order.status in ["Shipped","Delivered"]:
            return Response({
                "error":"Cannot cancel order"
            })
        
        order.status = "Cancelled"
        order.save()

        return Response({
             "message":"Order Cancelled"
        })


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(seld, request):

        order_id = request.data.get("order_id")

        order = Order.objects.get(id=order_id, user=request.user)

        razorpay_order = client.order.create({
            "amount":
            int(order.total_amount * 100),

            "currency":"INR",

            "payment_capture":1
        })

        return Response({
            "razorpay_order_id":razorpay_order["id"],

            "amount":razorpay_order["amount"],

            "key":settings.RAZORPAY_KEY_ID
        })


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = Order.objects.get(id=request.data.get("order_id"), user=request.user)

        order.payment_id = request.data.get("payment_id")

        order.is_paid = True

        order.save()

        return Response({
            "message":"Payment Successful"
        })


class AdminOrdersView(APIView):

    permission_classes = [IsAdminRole]

    def get(self, request):

        orders = Order.objects.all().order_by("-created_at")

        serializer = OrderSerializer(orders,many=True)

        return Response(serializer.data)


class UpdateOrderStatusView(APIView):

    permission_classes = [
        IsAdminRole
    ]

    def patch(self,request,order_id):

        order = Order.objects.get(id=order_id)

        new_status = request.data.get("status")

        valid_status = [

            "Pending",

            "Processing",

            "Shipped",

            "Delivered",

            "Cancelled"
        ]

        if new_status not in valid_status:

            return Response({
                "error":"Invalid Status"
            })

        order.status = new_status
        order.save()

        return Response({
            "message":"Status Updated",
            "status":order.status
        })