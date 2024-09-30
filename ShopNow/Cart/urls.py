from django.urls import path
from .models import *

from Cart.Backend.views import *
from Cart.FrontEnd.views import *


urlpatterns = [
    # Path to the API URLs
    path('getCart/',GetCartView.as_view(),name='getCart'), 
    path('addToCart/',AddCartView.as_view(),name='addToCart'), 
    path('deleteCart/<int:product_id>',DeleteCartView.as_view(),name='deleteCart'), 

    # path('addToCart/',AddcartView.as_view(),name='cart'),
    path('addProductInCart/<int:pk>',add_to_cart_frontend,name='addProductInCart'), 
    path('showCart/',show_cart,name='showCart'), 
    path('deletecartProduct/<int:product_id>',delete_prod_from_cart,name='deletecartProduct'), 
        
]