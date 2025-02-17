from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework import status 
from app.models import CustomUser,Product,Cart
from .serializers import ProductSerializer,CartSerializer


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
    return Response(serializer.data)


@api_view(['GET','POST'])
def product_view(request):
    ...



@api_view(['POST'])
def add_to_cart(request,productId):
    if request.user.is_authenticated:

        data = request.data
        user=request.user
        product = get_object_or_404(Product,id=productId)

        cart_item, created = Cart.objects.get_or_create(user=user, product=product, status=0)

        if not created:
            cart_item.quantity += 1
            cart_item.save()
            return Response({"message": "Cart updated successfully", "quantity": cart_item.quantity}, status=200)

        return Response({"message":"Product added to cart "},status=status.HTTP_201_CREATED)
        

    else:
        return Response({"message":"user need to login before cart"},status=status.HTTP_401_UNAUTHORIZED)
        
    
@api_view(['GET'])
def get_cart(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, status=0).select_related('product')
        serializer = CartSerializer(carts, many=True, context={'request': request})
        
        return Response(serializer.data, status=200)  # Directly returning the list

    return Response({'message': 'User not authenticated'}, status=401)















