from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework import status 
from app.models import CustomUser,Product
from .serializers import ProductSerializer


@api_view(["POST"])
def login_api(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password :
        return Response({"error": "Username and password required"}, status= status.HTTP_400_BAD_REQUEST)
    

    user = authenticate(username=username,password=password)



    if user :
        login(request,user)
        return Response({"message":"Login Successful" }, status=status.HTTP_200_OK)

    elif CustomUser.objects.filter(username=username).exists():

        return Response({"error":"Password doesnot match"},status=status.HTTP_401_UNAUTHORIZED)
    

    else :
        return Response({"error":"user doesnot exist "},status=status.HTTP_404_NOT_FOUND)
    



@api_view(['POST'])
def register_api(request):

    username = request.data.get("username")
    firstName = request.data.get("firstName")
    lastName = request.data.get("lastName")
    print(request.data)
    if len(firstName) < 2 or len(lastName) < 2:
        return Response ({"message":"Name must not be empty "},status = status.HTTP_400_BAD_REQUEST)
    

    if CustomUser.objects.filter(username=username).exists():

        return Response({"message":"username already exists "},status=status.HTTP_409_CONFLICT)
    
    else :
        password = request.data.get("password")
        user = CustomUser.objects.create_user(username=username,password=password)
        user.is_verified = False 
        user.first_name = firstName
        user.last_name = lastName
        user.save()
        return Response({"message":"User create successfully"},status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def trending_product(request):

    trending_products = Product.objects.order_by('-sold_count')[:10]  
    serializer = ProductSerializer(trending_products,many=True)
    return Response({"data":serializer.data})


@api_view(['GET','POST'])
def product_view(request):
    ...








