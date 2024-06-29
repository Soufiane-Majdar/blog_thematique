from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/<int:id>/', views.about, name="about"),
    path('about/', views.about, name="about"),
]