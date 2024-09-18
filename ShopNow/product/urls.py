from django.contrib import admin
from django.urls import path, include  # Correctly importing `include`
from product.models import product

from product.views import *

#for media urls we have to defin these urls





urlpatterns = [
    # Path to the API URLs
    path('product/',productView.as_view(),name='product'),    
    path('product/<int:pk>',productView.as_view(),name='product_with_id'),  
    path('search/<str:product_name>',searchApiByName.as_view(),name='search'),  

    #template paths
    path('listproduct/',ListProducts.as_view(),name='listProduct'),   
     path('deleteProduct/<int:pk>',delete_Product,name='deleteProduct'),
     path('add_product/',add_product,name='add_product'),
      path('update_product/<int:pk>',update_Product,name='update_Product'),
    path('products_list_user/',products_list_for_user,name='products_list_user'),
    path('search/',search,name='searchView'),
    #path('searchedProduct/',products_list_for_user,name='searchedProduct'),
]




