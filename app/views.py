from django.shortcuts import render, redirect 
from django. contrib.auth import logout
from django.contrib.auth.decorators import login_required


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



