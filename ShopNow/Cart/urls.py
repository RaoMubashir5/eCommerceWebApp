from django.urls import path
from .models import addToCart

from .views import *


urlpatterns = [
    # Path to the API URLs
   path('addToCart/',AddcartView.as_view(),name='cart'), 
   path('addToCart/<int:product_id>',AddcartView.as_view(),name='delete'),   
]