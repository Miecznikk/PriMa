from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import SendMessageForm
from EmailService.service import EmailService


@method_decorator(login_required, name='dispatch')
class MyMessages(View):
    template_name = 'messages/my_messages.html'

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user)
        return render(request, self.template_name, {
            'messages': messages
        })


@method_decorator(login_required, name='dispatch')
class MessageSendView(View):
    template_name = 'messages/send_message.html'

    def get(self, request):
        form = SendMessageForm(user=request.user)
        default_receiver = request.GET.get("default_receiver", None)
        if default_receiver is not None and default_receiver != request.user.id:
            try:
                if User.objects.filter(id=default_receiver).exists():
                    form.initial = {"receiver": default_receiver}
                    form.fields['receiver'].widget.attrs['disabled'] = True
                else:
                    pass
            except ValueError:
                pass
        return render(request, self.template_name, {
            "form": form
        })

    def post(self, request):
        form = SendMessageForm(request.POST, request.GET, user=request.user)
        form.fields['receiver'].required = False
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = get_object_or_404(User, id=int(request.GET.get("default_receiver")))
            message.save()
            EmailService.send_new_message_mail_to_user(request, message.receiver, request.user)
        else:
            return render(request, self.template_name, {
                "form": form
            })
        return redirect('messages:my_messages')


@method_decorator(login_required, name='dispatch')
class DeleteMessageView(View):
    redirect_to = 'messages:my_messages'

    def post(self, request, id):
        message = get_object_or_404(Message, id=id, receiver=request.user)
        message.delete()
        return redirect(self.redirect_to)
