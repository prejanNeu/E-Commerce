from django.shortcuts import render, redirect 
from django. contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from django.http import JsonResponse
@api_view(["GET"])
def esewa_success(request):
    return JsonResponse({"status": "success", "message": "Payment successful!"})

@api_view(["GET"])
def esewa_failure(request):
    return JsonResponse({"status": "failure", "message": "Payment failed!"})



def login_page(request):

    return render(request,"app/login_page.html")


def register_page(request):
    return render(request,"app/register_page.html")


def logout_page(request):

    logout(request.user)

def send_mail(request):
    ...


@login_required(login_url="login_page")
def dashboard_view(request):

    information = {}

    return render(request,"app/dashboard.html",{"information":information})


def home_page(request):
    
    return render(request,"app/home_page.html")



