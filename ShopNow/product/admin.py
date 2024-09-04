from django.contrib import admin
from .models import product
# Register your models here.

class customeAdmin(admin.ModelAdmin):
    list_display=('product_name','price','product_image','product_description')

admin.site.register(product,customeAdmin)