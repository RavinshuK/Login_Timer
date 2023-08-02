from django.contrib import admin
from django.urls import path, include
from loginapp import views

urlpatterns = [
    
    path("", views.index, name='loginapp'),
    path("login", views.loginUser, name='login'),
    path("logout", views.logoutUser, name='logout')
]