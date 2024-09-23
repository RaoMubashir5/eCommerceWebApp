from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenObtainPairView
from UserApp.views import *

urlpatterns=[
    path('register/',registerUser,name = 'registerUser'),
    path('gettoken/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('varify/', TokenVerifyView.as_view()),
    path('login/',loginUser,name = 'login'),
    path('user/',getUserName.as_view(),name = 'user'),
    path('user/<int:pk>',getUserName.as_view(),name = 'user'),    

    #Front end paths
    path('home/',home,name='home'),  
    path('all_users/',UserAdminFrontend.as_view(),name='all_users'),    
    path('single_user/<int:pk>',UserAdminFrontend.as_view(),name='single_user'),
    path('register_new/',registerFrontend,name='register_new'),
    path('login_user/',loginPage,name='login_user'),    
    path('update/<pk>',updateProfile,name='update'),
    path('delete/<pk>',deleteUser,name='delete'),   
    path('admin/',adminLogin,name='admin'),  
    path('admin_options/',adminOptions,name='admin_options'),
]