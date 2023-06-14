from django.shortcuts import render
from .forms import RegisterForm

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        form.save()
    form = RegisterForm()
    return render(request,'registration/sign_up.html', {'form': form})

# Create your views here.
