from django.shortcuts import render
from .models import Post

def Home(request):
    posts = Post.objects.all().order_by('-date_posted')  # 👈 Order by newest first
    return render(request, 'blog/home.html', {'posts': posts})

def about(request):
    return render(request,'blog/about.html',{"title":"About"})

def contact(request):
    return render(request,'blog/contact.html',{"title":"Contact"})



    # Create your views here.
