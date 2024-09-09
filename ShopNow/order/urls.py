from django.contrib import admin
from .views import orderApi
from django.urls import path

urlpatterns = [path('order/',orderApi.as_view(),name='order'),
               path('order/<int:pk>',orderApi.as_view(),name='order'),]
