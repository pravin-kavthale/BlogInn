from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    image=models.ImageField(default='profile/default.jpg',upload_to='profile')

    def __str__(self):
        return f"{self.user.username}Profile"

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img=Image.open(self.image.path)
        if img.width>300 or img.height>300:
            img.thumbnail((300, 300))
            img.save(self.image.path)