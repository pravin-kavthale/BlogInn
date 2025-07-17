from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path("", views.Home,name="blog-home"),
    path("about/",views.about,name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path("register/",user_views.register,name="user-register"),
    
]