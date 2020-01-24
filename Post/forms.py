from django.forms import ModelForm
from .models import Post, Reply
from django.forms import Textarea

class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content':Textarea(attrs={'cols':60,'rows':15}),
        }

class PostReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = '__all__'
        widgets = {
            'reply_body': Textarea(attrs={'cols':60,'rows':2})
        }