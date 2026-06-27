from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.permissions import IsAdminUser

from accounts.models import User
from products.models import Product
from orders.models import Order
# Create your views here.

class DashboardView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()

        total_products = Product.objects.count()

        total_orders = Order.objects.count()

        total_revenue = Order.objects.filter(is_paid=True).aggregate(total=Sum('total_amount'))['total']

        return Response({
              "total_users":total_users,

              "total_products":total_products,

              "total_orders":total_orders,

              "total_revenue":total_revenue
            })