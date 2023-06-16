from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from EmailService.service import EmailService
from EmailService.token import account_activation_token


from .forms import RegisterForm

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            EmailService.send_confirmation_mail_to_user(request,user,form.cleaned_data.get('email'))
            return HttpResponse("Check your mail to activate the account")
    form = RegisterForm()
    return render(request,'registration/sign_up.html', {'form': form})

# Create your views here.
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        return HttpResponse('Account activated succesfully')
    return HttpResponse('Activation link is incorrect or your account is already activated')
