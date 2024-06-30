from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/<int:id>/', views.about, name="about"),
    path('about/', views.about, name="about"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('add_publication/', views.add_publication, name='add_publication'),
    path('update-publication/<int:publication_id>/', views.update_publication, name='update_publication'),
    path('delete-publication/<int:publication_id>/', views.delete_publication, name='delete_publication'),
]