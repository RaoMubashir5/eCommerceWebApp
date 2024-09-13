from django.contrib import admin
from django.urls import path, include  # Correctly importing `include`
from product.models import product

from product.views import *

#for media urls we have to defin these urls





urlpatterns = [
    # Path to the API URLs
    path('product/',productView.as_view(),name='product'),    
    path('product/<int:pk>',productView.as_view(),name='product'),   

    #template paths
    path('listproduct/',ListProducts.as_view(),name='listProduct'),   
     path('deleteProduct/<int:pk>',delete_Product,name='deleteProduct'),
     path('add_product/',add_product,name='add_product'),
]