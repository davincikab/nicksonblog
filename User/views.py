from django.shortcuts import render
from .models import UserProfile

# Create your views here.
def myprofile(request):
    data = UserProfile.objects.get(user = 1)
    return render(request, 'user/profile.html', {'data':data})
