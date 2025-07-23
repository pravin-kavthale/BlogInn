from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView

)

from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class UserPostListView(ListView):
    model=Post
    template_name="blog/users_post.html"
    context_object_name = 'posts'
    paginate_by=5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
         
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context   

class PostListView(ListView):
    model=Post
    template_name="blog/home.html"
    context_object_name = 'posts'
    ordering=['-date_posted']

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content','image']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)\

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content','image']
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url="/"
    def test_func(self):
        post=self.get_object()
        if post.author==self.request.user:
            return True
        else:
            return False

def about(request):
    return render(request,'blog/about.html',{"title":"About"})

def contact(request):
    return render(request,'blog/contact.html',{"title":"Contact"})


