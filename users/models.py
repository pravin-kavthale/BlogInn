from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    gender = models.CharField(default='Other', max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    age = models.IntegerField(null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
    summary = models.TextField(max_length=500, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}Profile"

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img=Image.open(self.image.path)
        if img.width>300 or img.height>300:
            img.thumbnail((300, 300))
            img.save(self.image.path)