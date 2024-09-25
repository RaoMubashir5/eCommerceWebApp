from .Backend.views import *
from .Frontend.views import *
from django.urls import path

urlpatterns = [
               path('order/', GetAllOrderApi.as_view(), name = 'order'),
               path('singleOrder/<int:pk>', GetOrderApi.as_view(), name = 'singleOrder'),
               path('addOrder/<int:pk>', AddOrderApi.as_view(), name = 'addOrder'),
               path('all_order/', UserOrders.as_view(), name = 'allorder'),   
               path('user_order/<int:pk>', UserOrders.as_view(), name = 'userorder'),
               
               path('placeOrder/<int:pk>', place_order, name = 'placeOrder'),
               path('orderHistory/', all_orders_history, name = 'orderHistory'),
               path('orderHistory/<int:pk>', single_orders_history, name = 'orderHistory')]
