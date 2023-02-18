from django.urls import path 
from user import views 

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
]
