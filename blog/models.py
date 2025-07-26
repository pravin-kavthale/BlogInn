from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(default="background.jpg",upload_to='blog')
    liked_users = models.ManyToManyField(User, through='Like', related_name='liked_posts')

    def __str__(self):
        return self.title
   
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
    
    def total_likes(self):
        return self.like_set.filter(liked=Ture).count()
    

class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    liked=models.BooleanField(default=False)
    timestamp=models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(max_length=200)
    created_at=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.sender.username} comment on {self.post.title}"

