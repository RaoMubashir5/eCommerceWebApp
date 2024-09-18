from django.contrib import admin
from .models import order,OrderItem
class customOrder(admin.ModelAdmin):
    list_display=('ordered_by_user','total_bill','order_date')
    list_filter=('ordered_by_user','order_date')

# Register your models here.

admin.site.register(order,customOrder)
class customOrderItem(admin.ModelAdmin):
    list_display=('id','order','product','quantity','price')
    list_filter=('order','id')

# Register your models here.

admin.site.register(OrderItem,customOrderItem)
