from django.contrib import admin
from .models import Product

class CustomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'product_image', 'product_description')

admin.site.register(Product, CustomeAdmin)