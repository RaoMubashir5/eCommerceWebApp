from django.contrib import admin
from .models import cartModel,addToCart
# Register your models here.

class customadmin(admin.ModelAdmin):
    list_display=('id','user_of_cart',)
    list_filter=('user_of_cart',)
admin.site.register(cartModel,customadmin)

class customAddCartadmin(admin.ModelAdmin):
    list_display=('id','cart_product','cart','product_quantity',)
    list_filter=('cart','cart_product',)

admin.site.register(addToCart,customAddCartadmin)