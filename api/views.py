from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework import status 



@api_view(["POST"])
def api_login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password :
        return Response({"error": "Username and password required"}, status= status.HTTP_400_BAD_REQUEST)

    user = authenticate(username= username,password=password)

    if user :
        login(request,user)
        return Response({"message":"Login Successful" }, status=status.HTTP_200_OK)

    elif User.objects.filter(username=username).exists():

        return Response({"error":"Password doesnot match"},status=status.HTTP_401_UNAUTHORIZED)
    

    else :
        return Response({"error":"user doesnot exist "},status=status.HTTP_404_NOT_FOUND)



