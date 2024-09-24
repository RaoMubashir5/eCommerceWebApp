from django.urls import path
from .models import *

from .views import *


urlpatterns = [
    # Path to the API URLs
    path('addToCart/',AddcartView.as_view(),name='cart'), 
    path('addToCart/<int:product_id>',AddcartView.as_view(),name='delete'), 
    # path('addToCart/',AddcartView.as_view(),name='cart'),
    path('addProductInCart/<int:pk>',add_to_cart_frontend,name='addProductInCart'), 
    path('showCart/',show_cart,name='showCart'), 
     path('deletecartProduct/<int:product_id>',delete_prod_from_cart,name='deletecartProduct'), 
        
]