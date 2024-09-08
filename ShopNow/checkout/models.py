from django.db import models

from UserApp.models import Webuser


# Create your models here.

class checkoutPage(models.Model):
    full_name=models.CharField(max_length=40,null=False,blank=False)
    address=models.CharField(max_length=60,null=False,blank=False)
    city=models.CharField(max_length=30,blank=False)
    province=models.CharField(max_length=30,blank=False)
    zip_code=models.CharField(max_length=25,blank=False)
    country=models.CharField(max_length=30,blank=False)




