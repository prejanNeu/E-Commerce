from django.urls import path 
from. import views 


urlpatterns = [
    path("api/login/post/",views.login_api,name="login")
]