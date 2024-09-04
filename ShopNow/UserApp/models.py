from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Webuser(AbstractUser):
    
    created_by=models.OneToOneField('self',null=True, on_delete=models.CASCADE)
    email=models.EmailField(null=False,blank=False,unique=True)
    
    def __str__(self):
        return f'{self.username}'
    class Meta:
        verbose_name='webUser'

        


