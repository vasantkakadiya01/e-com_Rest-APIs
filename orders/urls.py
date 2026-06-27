# orders/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/',CheckoutView.as_view()),
    path('my-orders/',MyOrdersView.as_view()),
    path('<int:order_id>/',OrderDetailView.as_view()),
    path('<int:order_id>/cancel/',CancelOrderView.as_view()),
    path('create-payment/',CreatePaymentView.as_view()),
    path('verify-payment/',VerifyPaymentView.as_view()),
    path('admin/orders/',AdminOrdersView.as_view()),
    path('admin/orders/<int:order_id>/status/',UpdateOrderStatusView.as_view()),
]