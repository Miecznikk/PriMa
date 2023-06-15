from django.urls import path
from . import views
from django.contrib.auth import views as v
from .forms import LoginForm

app_name = 'users'

urlpatterns = [
    path('sign_up/', views.sign_up, name='register'),
    path('login/',v.LoginView.as_view(template_name="registration/login.html",authentication_form=LoginForm),
         name='login'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate')
]