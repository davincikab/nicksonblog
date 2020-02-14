from .models import Post, Reply
from .forms import CreatePostForm,PostReplyForm

from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime

def home(request):
    return render(request,'index.html')

def archives(request):
    date = timezone.now() - datetime.timedelta(days = 1)
    data = Post.objects.filter(created_on__gte = date).order_by('created_on')
    print(data)
    return render(request, 'archives.html', {'data':data})

# Get all the posts
class PostListView(ListView):
    # Add time filter
    model = Post
    context_object_name = 'posts'
    template_name = 'index.html'
    paginate_by = 2

    def get_queryset(self):
        date = timezone.now() - datetime.timedelta( days = 150)
        q = self.request.GET.get('q')
        queryset = search_post(self.request, q,date)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        date = timezone.now() - datetime.timedelta( days = 150)
        context['archives'] = Post.objects.filter(created_on__lte = date )
        return context

# Get the post data
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = Post.objects.filter(pk=self.object.pk)

        context['nexts'] = Post.objects.filter(pk = self.object.pk+1)
        context['previous'] = Post.objects.filter(pk=self.object.pk-1)
        context['related'] = Post.objects.exclude(pk=self.object.pk)\
                                    .filter(genre__icontains=subject[0].genre)\
                                    .filter(published=True)
    
        return context
    
    def get_queryset(self):
        #Overide: to add the comments for each post
        context = super().get_queryset()
        # context['reply'] = super().get_queryset().prefetch_related('post')
        return context

# Create a post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html' 
    context_object_name = 'post'
    form_class = CreatePostForm

# Update the data
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_create.html'
    context_object_name = 'post' 
    fields = '__all__'

# Delete a post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('list-view')

#Search post: Implemnet a Search Ranking using SearcVector
def search_post(request,query,date):
    if(query == None):
        return Post.objects.all().filter(published=True).order_by('created_on')
    else:
        return Post.objects.filter(title__icontains=query).filter(published=True).order_by('created_on')

# Refactor these section
def render_reply_form(request):
    if request.method == 'POST':
        form = PostReplyForm(request.POST)
        if form.is_valid():
            form.save()
            #Add a message and list of replies for the given post
            replies = serialize('json', Reply.objects.filter(post=request.POST['post']))
            return HttpResponse(replies)
    else:
        #return existing replies
       replies = serialize('json', Reply.objects.filter(post=request.GET.get('post')).order_by('-reply_at'))
       return HttpResponse(replies)


# Add message framework
# Cookies and sessions
# Change the url to: year/ month/ post.html rather than post id 
# work with uuid
# Test the views: Make sure they return the correct url
