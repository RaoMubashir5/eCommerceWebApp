from django.urls import path
from product.Backend.views import *
from product.Frontend.views import *

urlpatterns = [
              path('product/', GetProducts.as_view(), name = 'product'),    
              path('productDetail/<int:pk>', GetProductDetail.as_view(), name = 'product_detail'),  
              path('addProduct/', AddProductApi.as_view(), name = 'product_add'),
              path('updateProduct/<int:pk>', UpdateProductApi.as_view(), name = 'product_update'),
              path('deleteProduct/<int:pk>', DeleteProductApi.as_view(), name = 'product_delete'),
              path('search/<str:product_name>', SearchApiByName.as_view(), name = 'search'), 
              #   Frontend urls 

              path('listproduct/', ListProducts.as_view(), name = 'listProduct'),   
              path('delete_product/<int:pk>', delete_Product, name = 'deleteProduct'),
              path('add_product/', add_product, name = 'add_product'),
              path('update_product/<int:pk>', update_Product, name = 'update_Product'),
              path('products_list_user/', products_list_for_user, name = 'products_list_user'),
              path('search/', search, name = 'searchView'),
              ]





