from django.db import models

from UserApp.models import Webuser

from Cart.models import cartModel
from product.models import product
# Create your models here.

class order(models.Model):
    ordered_by_user=models.ForeignKey(Webuser,on_delete=models.CASCADE,related_name='user_orders')
    cart=models.ForeignKey(cartModel,on_delete=models.CASCADE,related_name='order_cart_detail')
    total_bill=models.FloatField(blank=True,null=False)
    order_date=models.DateTimeField(auto_now_add=True)

class orderItem(models.Model):
    order = models.ForeignKey(order, related_name='order_items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)  # Store product name at the time of purchase
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Store product price at purchase
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product_name}"



