from django import forms
from .models import Message
from django.contrib.auth.models import User


class SendMessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), label='Message to: ')

    class Meta:
        model = Message
        fields = ['receiver', 'title', 'description']
        labels = {
            'receiver': "Message to:",
            'title': "Title",
            'description': "Description"
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(SendMessageForm, self).__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.all().exclude(id=user.id)
