from django.urls import path
from product.views import *

urlpatterns = [
              path('product/', ProductView.as_view(), name = 'product'),    
              path('product/<int:pk>', ProductView.as_view(), name = 'product_with_id'),  
              path('search/<str:product_name>', SearchApiByName.as_view(), name = 'search'),  
              path('listproduct/', ListProducts.as_view(), name = 'listProduct'),   
              path('deleteProduct/<int:pk>', delete_Product, name = 'deleteProduct'),
              path('add_product/', add_product, name = 'add_product'),
              path('update_product/<int:pk>', update_Product, name = 'update_Product'),
              path('products_list_user/', products_list_for_user, name = 'products_list_user'),
              path('search/', search, name = 'searchView')]





