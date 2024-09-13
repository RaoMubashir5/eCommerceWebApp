from django.contrib import admin
from django.urls import path,include

from UserApp.views import *

from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView,TokenObtainPairView


#create object of the DefaultRouter
routers=DefaultRouter()

#register the route with the ViewSet class



urlpatterns=[
    path('register/',registerUser,name='registerUser'),
    path('gettoken/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('varify/', TokenVerifyView.as_view()),
    path('login/',loginUser,name='login'),
    path('user/',get_register_users.as_view(),name='user'),
    path('user/<int:pk>',get_register_users.as_view(),name='user'),    

    #Front end paths
    path('home/',home,name='home'),  
    path('all_users/',UserAdminFrontend.as_view(),name='all_users'),    
    path('single_user/<int:pk>',UserAdminFrontend.as_view(),name='single_user'),
    path('register_new/',registerFrontend,name='register_new'),
    path('login_user/',login_page,name='login_user'),    
    path('update/<pk>',update_profile,name='update'),
    path('delete/<pk>',delete_user,name='delete'),   
    path('admin/',admin_login,name='admin'),  
    path('admin_options/',admin_options,name='admin_options'),
]