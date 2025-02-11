from django.urls import path 
from. import views 


urlpatterns = [
    path("api/login/post/",views.login_api,name="login"),
    path("api/register/post/",views.register_api,name="register"),
    path("api/product/trending",views.trending_product,name="trending_product"),
    
]