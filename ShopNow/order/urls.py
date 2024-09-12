from django.contrib import admin
from .views import orderApi,userOrders
from django.urls import path

urlpatterns = [path('order/',orderApi.as_view(),name='order'),
               path('order/<int:pk>',orderApi.as_view(),name='order'),
               path('all_order/',userOrders.as_view(),name='allorder'),
               path('user_order/<int:pk>',userOrders.as_view(),name='userorder'),
               ]
