from django.db import models

class product(models.Model):
    product_name=models.CharField(max_length=30,unique=True,null=False,blank=False)
    product_description=models.TextField(max_length=100,blank=False,null=False,unique=True)
    price=models.FloatField(null=False,blank=False)
    product_image=models.ImageField(upload_to="productImage")

