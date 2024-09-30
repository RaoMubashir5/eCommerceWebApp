from django.db import models
from django.contrib.auth.models import AbstractUser

class Webuser(AbstractUser):
    created_by = models.OneToOneField('self', null = True, on_delete = models.CASCADE)
    email = models.EmailField(null = False, blank = False, unique = True)
    address = models.CharField(null = False, blank = False, default = 'Lahore', max_length = 100)

    def __str__(self):
        return f'{self.username}'
    class Meta:
        verbose_name = 'webUser'

        


