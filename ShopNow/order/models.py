from django.db import models

from UserApp.models import Webuser

from checkout.models import checkoutPage
from product.models import product
# Create your models here.

class order(models.Model):
    ordered_by_user=models.ForeignKey(Webuser,on_delete=models.CASCADE,related_name='user_orders')
    checkout_info=models.ForeignKey(checkoutPage,on_delete=models.CASCADE,related_name='checking_out_order_detail')
    total_bill=models.FloatField(blank=True,null=False)
    order_date=models.DateTimeField(auto_now=True)



class OrderItem(models.Model):
    order = models.ForeignKey(order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store product price at the time of purchase

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

