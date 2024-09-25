from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenObtainPairView
from UserApp.Backend.views import *
from UserApp.FrontEnd.views import *

urlpatterns=[
    path('register/', register_user,name = 'registerUser'),
    path('gettoken/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('varify/', TokenVerifyView.as_view()),
    path('login/', login_user,name = 'login'),
    path('user/', GetRegisterterdUsers.as_view(), name = 'user'),
    path('userDetail/<int:pk>', GetSingleUser.as_view(), name = 'userDetail'),
    path('updateUser/<int:pk>', UpdateUser.as_view(), name = 'updateUser'),
    path('DeleteUser/<int:pk>', DeleteUser.as_view(), name = 'DeleteUser'),

    #Front end paths
    path('home/', home, name = 'home'),  
    path('all_users/', AllUsersDetails.as_view(), name = 'all_users'),    
    path('single_user/<int:pk>', SingleUserDetails.as_view(), name = 'single_user'),
    path('register_new/', user_registeration,name = 'register_new'),
    path('login_user/', login_page,name = 'login_user'),    
    path('update/<pk>', update_profile, name = 'update'),
    path('delete/<pk>', delete_user, name = 'delete'),   
    path('admin/', admin_login, name = 'admin'),  
    path('admin_options/', admin_options, name = 'admin_options'),
]