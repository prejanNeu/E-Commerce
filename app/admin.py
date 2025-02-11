from django.contrib import admin

from .models import Product, CustomUser,Cart,Order,Category



admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category)
