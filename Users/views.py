from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from EmailService.service import EmailService
from EmailService.token import account_activation_token
from django.views import View
from .models import InvestorUser
from .forms import RegisterForm, ProfileEditForm


class SignUp(View):
    template_name = 'registration/sign_up.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            EmailService.send_confirmation_mail_to_user(request, user, form.cleaned_data.get('email'))
            return HttpResponse("Check your mail to activate the account")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Account activated succesfully')
    return HttpResponse('Activation link is incorrect or your account is already activated')


class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, id):
        investor = get_object_or_404(InvestorUser, id=id)
        return render(request, self.template_name, {
            "investor": investor
        })


class ProfileEditView(View):
    tempalte_name = 'users/profile_edit.html'

    def get(self, request, id):
        if request.user.investoruser.id == id:
            investor = get_object_or_404(InvestorUser, id=id)
            initial_data = {
                "company_name": investor.company_name,
                "email": investor.user.email,
                "phone_number": investor.phone_number,
                "company_logo": investor.company_logo
            }
            form = ProfileEditForm(initial=initial_data, instance=investor)
            return render(request, self.tempalte_name, {
                "investor": investor,
                "form": form
            })
        else:
            raise PermissionDenied

    def post(self, request, id):
        if request.user.investoruser.id == id:
            investor = get_object_or_404(InvestorUser, id=id)
            form = ProfileEditForm(request.POST, request.FILES, instance=investor)
            if form.is_valid():
                cd = form.cleaned_data
                investor = form.save(commit=False)
                investor.user.email = cd.get("email")
                investor.user.save()
                investor.save()
                return redirect('users:profile', investor.id)
            else:
                return render(request, self.tempalte_name, {
                    "investor": investor,
                    "form": form
                })
        else:
            raise PermissionDenied
