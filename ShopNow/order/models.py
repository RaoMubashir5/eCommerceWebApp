from django.db import models

from UserApp.models import Webuser

from Cart.models import cartModel
from product.models import product
# Create your models here.

class order(models.Model):
    ordered_by_user=models.ForeignKey(Webuser,on_delete=models.CASCADE,related_name='user_orders')
    total_bill=models.FloatField(blank=True,null=False,default=0.0)
    order_date=models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField() 
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"

