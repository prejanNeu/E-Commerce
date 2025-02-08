from django.urls import path 
from. import views 


urlpatterns = [
    path("api/login/post/",views.api_login,name="login")
]