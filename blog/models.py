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

    def __str__(self):
        return self.title
   
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    liked=models.BooleanField(default=False)