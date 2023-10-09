from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.db import transaction
from captcha.fields import ReCaptchaField
from .models import CustomerUser


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'validate', }))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    captcha = ReCaptchaField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        help_texts = {
            'username': None,
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        customer_user = CustomerUser.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
