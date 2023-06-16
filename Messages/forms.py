from django import forms
from .models import Message
from django.contrib.auth.models import User

class SendMessageForm(forms.ModelForm):

    receiver = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['title','description','receiver']
        labels = {
            'title' : "Title",
            'description' : "Description",
            'receiver' : "Message to:"
        }