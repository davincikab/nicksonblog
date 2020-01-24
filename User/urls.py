from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import myprofile
urlpatterns = [
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('profile', myprofile, name='profile')
]
