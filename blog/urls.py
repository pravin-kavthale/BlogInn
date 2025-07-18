from django.urls import path
from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.Home,name="blog-home"),
    path("about/",views.about,name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path("register/",user_views.register,name="user-register"),
    
]