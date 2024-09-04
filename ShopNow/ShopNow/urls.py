"""
URL configuration for ShopNow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Correctly importing `include`

# # Import views from your app
# from PracApp import views  # Assuming `PracApp` is your app's name

# Import views from the `api` app or specific views if necessary
from UserApp.views import *  # Importing all views from `api.views`
from product.views import *  

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Path to the admin page
    path('admin/', admin.site.urls), #it should be either in the specific app urls or not .
    
    # Path to the API URLs
    path('api/', include('UserApp.urls')),  # Assuming you have `api/urls.py` for your API routes
    path('api/', include('product.urls')),

    path('mub/',include('rest_framework.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
