from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Like
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from users.models import Notification
from django.db.models import Count,Q
from .forms import commentForm

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
    
    def get_queryset(self): #get the query set result from the database filter based on current user 
        return Post.objects.annotate(  #anotate adds extra data ike count 
            total_likes=Count('like', filter=Q(like__liked=True)) # Q executed and or not query by default it is and 
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            liked_posts = Like.objects.filter(user=self.request.user, liked=True).values_list('post_id', flat=True)
        else:
            liked_posts = []
        context['liked_posts'] = liked_posts
        return context

class PostDetailView(DetailView):
    model=Post
    template_name='blog/post_detail.html'
    context_object_name='post'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        post=self.get_object()
        context['comment']=post.comment_set.all().order_by('-created_at')
        context['form']=commentForm()
        return context

    def post(self,request,*args,**kwargs):
        self.object=self.get_object()
        post=self.object
        form=commentForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                comment=form.save(commit=False)
                comment.post=post
                comment.sender=request.user
                comment.save()
                Notification.objects.create(
                    blog=post,
                    sender=request.user,
                    receiver=post.author,
                    type='Comment',
                    message=f"{request.user.username} Commented on your post: {post.title} | Comment:{comment.content}",
                    action_url=f'/post/{post.id}/'
                )
                return redirect('post-detail',pk=self.object.pk)
            return redirect('login')

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content','image']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

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

@login_required
def like_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    isliked=False

    like = post.like_set.filter(user=request.user).first()
    if like:
        like.liked = not like.liked
        isliked = like.liked
        like.save()
    else:
        Like.objects.create(user=request.user, post=post, liked=True)
        isliked = True
        
 
    if isliked and post.author!=request.user:
        Notification.objects.create(
            sender=request.user,
            receiver=post.author,
            message=f"{request.user.username} liked your post: {post.title}",
            blog=post,
            type='like',
            action_url=f'/post/{post.id}/'
        )

    return redirect('post-detail',pk=pk)

