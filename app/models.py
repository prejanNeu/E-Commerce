from django.db import models
from django.contrib.auth.models import AbstractUser
import os 
from django.conf import settings


class CustomUser(AbstractUser):

    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username 
    

class Category(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name 
    

class Product(models.Model):
    name = models.CharField(max_length=40,blank=False,null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    description = models.CharField(max_length=600,default='')
    image= models.ImageField(upload_to='products',null=True,blank=False)
    stock = models.PositiveIntegerField(blank=False,default=1)
    category = models.ForeignKey(Category,default=1,on_delete=models.CASCADE)
    sold_count = models.PositiveIntegerField(default=0)

    def __str__(self):

        return self.name
    
    def delete(self, *args, **kwargs):
        # Delete image file from storage before deleting the Product instance
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
            if os.path.exists(image_path):
                os.remove(image_path)

        super().delete(*args, **kwargs)



class Cart(models.Model):
    ...

class Order(models.Model):

    ...


