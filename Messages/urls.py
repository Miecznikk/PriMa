from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    path('messages/',views.my_messages,name='my_messages'),
    path('messages/send/',views.send_message,name='send_message')
]