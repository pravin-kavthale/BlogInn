from django.urls import path,include

from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views

from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CommentDeleteView
    )


urlpatterns = [
    path("", PostListView.as_view(),name="blog-home"),
    path("post/<int:pk>/",PostDetailView.as_view(),name="post-detail"),
    path("users/<str:username>/",UserPostListView.as_view(),name="user-posts"),

    path("about/",views.about,name='blog-about'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name='post-delete'),
    path('contact/', views.contact, name='blog-contact'),

    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),

    path('profile/', user_views.profile, name='profile'),
    path("register/",user_views.register,name="user-register"),
    path('profileUpdate/',user_views.profileUpdate,name='profileUpdate'),

    path('like/<int:pk>/',views.like_post,name='like_post'),
    path('notification/',user_views.notification,name='notification'),

    path('comment/<int:pk>/delete',CommentDeleteView.as_view(),name='comment-delete'),

    
]