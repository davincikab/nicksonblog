from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.urls import reverse
from PIL import Image
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    genre_choice = (
        ('GV', 'Governance'),
        ('BG', 'Budget'),
        ('DC', 'Democracy')
    )

    title = models.CharField(max_length=150)
    content = models.TextField(default='')
    created_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    genre = models.CharField(choices=genre_choice, max_length=15)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_photo = models.ImageField(upload_to="cover_photos/",default="2016.PNG",blank=True)
    published = models.BooleanField(default=False)

    # Format content to markdown
    def format_content(self):
        return markdownify(self.content)
    
    # Display the first 200 words
    def truncate_content(self):
        return markdownify(self.content[:400] + ' ...')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={'pk':self.pk})
    
    # Overide the save method: make_aware(self.created_on)
    class Meta:
        # db_table = 'post'
        ordering = ['-created_on']


class Reply(models.Model):
    name = models.CharField(max_length=50, blank=False, default='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    reply_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    reply_body = models.TextField()
    # user = models.ForeignKey(, verbose_name=_(""), on_delete=models.CASCADE)

    def __str__(self):
        return self.reply_body[:20]
    
    class Meta:
        ordering = ['-reply_at']





