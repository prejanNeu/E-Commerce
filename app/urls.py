from django.urls import path 
from . import views 

urlpatterns = [
    path("",views.home_page,name="home_page"),
    path("login/",views.login_page,name="login_page"),
    path("logout/",views.logout_page,name="logout_page"),
    path("send_mail/",views.send_mail,name='send_mail'),
    path("register/",views.register_page,name="register_page"),

]