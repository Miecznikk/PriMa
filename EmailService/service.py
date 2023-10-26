from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token
from django.utils.safestring import mark_safe


class EmailService:

    @staticmethod
    def send_confirmation_mail_to_user(request, user, email):
        current_site = get_current_site(request)
        mail_subject = f"{user.first_name}, activate your account!"
        message = render_to_string('email_templates/acc_active_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        email = EmailMessage(mail_subject, message, to=[email])
        email.send()

    @staticmethod
    def send_email_to_user(user, subject, text):
        message = render_to_string('email_templates/text_email.html', {
            'text': text
        })
        email = EmailMessage(subject, message, to=[user.email])
        email.send()

    @staticmethod
    def send_new_message_mail_to_user(request, user, message_from):
        current_site = get_current_site(request)
        mail_subject = f"New message from {message_from}"
        message = mark_safe(render_to_string("email_templates/new_message.html", {
            'user': user,
            'domain': current_site,
            'message_from': message_from
        }))
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

    @staticmethod
    def send_apartment_available_email_to_user(request, user, apartment_url):
        current_site = get_current_site(request)
        mail_subject = f"New apartment matching your recent search"
        message = mark_safe(render_to_string("email_templates/apartment_availible.html",{
            "user": user,
            "domain": current_site,
            "apartment_url": apartment_url
        }))
        email = EmailMessage(mail_subject,message, to=[user.email])
        email.send()