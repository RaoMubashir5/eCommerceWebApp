from django.contrib import admin
from .models import Order
from .models import OrderItem

class customOrder(admin.ModelAdmin):
    list_display=('ordered_by_user', 'total_bill', 'order_date')
    list_filter=('ordered_by_user', 'order_date')

class customOrderItem(admin.ModelAdmin):
    list_display=('id', 'order', 'product', 'quantity', 'price')
    list_filter=('order', 'id')

admin.site.register(Order,customOrder)
admin.site.register(OrderItem,customOrderItem)
