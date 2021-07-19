from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/', views.handleSignUp, name="handleSignUp"),
    path('login/', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('query/', views.query, name="query"),
    path('query_set/', views.query_set, name="query_set"),
    path('delete/<int:slug>',views.delete_,name="delete")
]