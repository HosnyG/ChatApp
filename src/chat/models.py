from django.db import models
from enum import Enum
from datetime import datetime
import json

# from django.core import serializers
    

class Message(models.Model):

    username = models.TextField()
    room = models.TextField()
    body = models.TextField()
    created = models.DateTimeField()

    def getByRoom(room_name):
        return Message.objects.filter(room = room_name).order_by('-created')


    def createOne(username,room,body):
        message = Message.objects.create(
            username = username,
            room = room,
            body = body,
            created = datetime.now()
        )
        return message
    
