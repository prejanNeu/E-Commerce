from django.shortcuts import render, redirect 


def login_page(request):
    

    return render(request,"app/login_page.html")
