from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)


    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username 
    

class Product(models.Model):
    ...


class Cart(models.Model):
    ...

class Order(models.Model):

    ...


