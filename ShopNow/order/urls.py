from django.contrib import admin
from .views import OrderApi,UserOrders,place_order,orders_history
from django.urls import path

urlpatterns = [
               path('order/', OrderApi.as_view(), name = 'order'),
               path('order/<int:pk>', OrderApi.as_view(), name = 'order'),
               path('all_order/', UserOrders.as_view(), name = 'allorder'),
               path('user_order/<int:pk>', UserOrders.as_view(), name = 'userorder'),
               path('placeOrder/<int:pk>', place_order, name = 'placeOrder'),
               path('orderHistory/', orders_history, name = 'orderHistory'),
               path('orderHistory/<int:pk>', orders_history, name = 'orderHistory')]
