from django.urls import path
from .views import *


urlpatterns = [
    path('add/',AddToCartView.as_view()),
    path('view/',ViewCartView.as_view()),
    path('remove/<int:item_id>/',RemoveCartItemView.as_view()),
    path('wishlist/add/',AddToWishlistView.as_view()),
    path('wishlist/view/',ViewWishlistView.as_view()),
    path('update/', UpdateCartItemView.as_view()),
]