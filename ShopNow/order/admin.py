from django.contrib import admin
from .models import order
class customOrder(admin.ModelAdmin):
    list_display=('ordered_by_user','checkout_info','total_bill','order_date')
    list_filter=('ordered_by_user','order_date')

# Register your models here.

admin.site.register(order,customOrder)
