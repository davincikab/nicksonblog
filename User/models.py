from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class UserProfile(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    cover_photo  = models.ImageField(upload_to='upload_to/')
    description = models.CharField(max_length=200)

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.cover_photo.path)
        if(img.height > 300 or img.width > 300):
            image_size = (300,300)
            img.thumbnail(image_size)
            img.save(self.cover_photo.path)
