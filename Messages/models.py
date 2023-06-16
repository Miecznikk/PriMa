from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='sender',null=True)
    receiver = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='receiver',null=True)

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

    created = models.DateTimeField(auto_now=True)

# Create your models here.
