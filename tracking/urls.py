from django.urls import path
from .views import Input

urlpatterns = [
    path ('', Input, name= "input"),
    
    
]
