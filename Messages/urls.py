from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    path('messages/', views.MyMessages.as_view(), name='my_messages'),
    path('messages/send/', views.MessageSendView.as_view(), name='send_message'),
    path('messages/delete/<int:id>', views.DeleteMessageView.as_view(), name='delete_message')
]
