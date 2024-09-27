from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from UserApp.Backend.views import * 
from product.Backend.views import *  
from Cart.Backend.views import *
from order.Backend.views import *

urlpatterns = [
                path('admin/', admin.site.urls),
                path('api/', include('UserApp.urls')),
                path('api/', include('product.urls')),
                path('api/', include('Cart.urls')),
                path('api/',include('order.urls')),
             ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
