from django.db import models

from UserApp.models import Webuser

from checkout.models import checkoutPage
# Create your models here.

class order(models.Model):
    ordered_by_user=models.ForeignKey(Webuser,on_delete=models.CASCADE,related_name='user_orders')
    checkout_info=models.ForeignKey(checkoutPage,on_delete=models.CASCADE,related_name='checking_out_order_detail')
    total_bill=models.FloatField(blank=True,null=False)
    order_date=models.DateTimeField(auto_now=True)




