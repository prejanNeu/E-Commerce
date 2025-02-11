from django.contrib.auth.models import User 
from rest_framework.serializers import ModelSerializer
from app.models import Product


class UserSerializer(ModelSerializer):


    class Meta:

        model = User 
        fields = ["id","username","password"]
        extra_kwargs = {"password":{"write_only":True}} 


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','name','price','description','image','stock','category','sold_count']