from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import gettext as _

gender_choices = (
    ("male", "male"),
    ("female", "female"),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    ethnicity = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(choices=gender_choices, max_length=30, null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    preference = models.TextField(max_length=500, blank=True, null=True)


    def __str__(self):
        return f'{self.user.username} profile'

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()


class Like(models.Model):
    created_on = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Catfish(models.Model):
    created_on = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver',on_delete=models.CASCADE)
    text = models.TextField(max_length=500, null=False, blank=False)
    created_on = models.DateField(auto_now_add=True)

class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    has_unread = models.BooleanField(default=False)

class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='photos/', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)