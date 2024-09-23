from django.contrib import admin
from django.urls import path, include
from UserApp.views import * 
from product.views import *  
from django.conf import settings
from django.conf.urls.static import static
from Cart.views import *
from order.views import *
urlpatterns = [
                path('admin/', admin.site.urls),
                path('api/', include('UserApp.urls')),
                path('api/', include('product.urls')),
                path('api/', include('Cart.urls')),
                path('api/',include('order.urls')),
             ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
