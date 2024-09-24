from django.contrib import admin
from .models import CartModel
from .models import AddToCart

class customadmin(admin.ModelAdmin):
    list_display = ('id', 'user_of_cart',)
    list_filter = ('user_of_cart',)

class customAddCartadmin(admin.ModelAdmin):
    list_display = ('id', 'cart_product', 'cart', 'product_quantity',)
    list_filter = ('cart', 'cart_product',)

admin.site.register(CartModel, customadmin)
admin.site.register(AddToCart, customAddCartadmin)