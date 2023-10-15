from django.shortcuts import render
from django.views import View

from .models import Message
from .forms import SendMessageForm


class MyMessages(View):
    def get(self, request):
        messages = Message.objects.filter(receiver=request.user)
        return render(request, 'messages/my_messages.html', {
            'messages': messages
        })
def send_message(request):
    if request.method == "POST":
        form = SendMessageForm(request.POST)
        message = form.save(commit=False)
        message.sender = request.user