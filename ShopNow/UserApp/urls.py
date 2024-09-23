from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenObtainPairView
from UserApp.views import *

urlpatterns=[
    path('register/',register_user,name = 'registerUser'),
    path('gettoken/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('varify/', TokenVerifyView.as_view()),
    path('login/',login_user,name = 'login'),
    path('user/',RegisteredUsers.as_view(),name = 'user'),
    path('user/<int:pk>',RegisteredUsers.as_view(),name = 'user'),    

    #Front end paths
    path('home/',home,name='home'),  
    path('all_users/',UserAdminFrontend.as_view(),name='all_users'),    
    path('single_user/<int:pk>',UserAdminFrontend.as_view(),name='single_user'),
    path('register_new/',user_registeration_frontend,name='register_new'),
    path('login_user/',login_page,name='login_user'),    
    path('update/<pk>',update_profile,name='update'),
    path('delete/<pk>',delete_user,name='delete'),   
    path('admin/',admin_login,name='admin'),  
    path('admin_options/',admin_options,name='admin_options'),
]