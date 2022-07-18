from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class Guest(models.Model):
    GUEST_STATUS = (
        ('INV', 'Invited'),
        ('NO', 'Not going'),
        ('PSBL', 'Possible going'),
        ('YES', 'Going')        
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    hash = models.CharField(max_length=30)
    status = models.CharField(max_length=5, choices=GUEST_STATUS, default=GUEST_STATUS[0][0])
    email = models.CharField(max_length=500, null=True)
    email_confirmed = models.BooleanField(default=False)


class GuestEquipment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_car = models.BooleanField(default=False)
    mats_cnt = models.IntegerField(default=0)
    tents_cnt = models.IntegerField(default=0)


class Message(models.Model):
    html_text = models.TextField()
    date_created = models.DateField(auto_now_add=True)
