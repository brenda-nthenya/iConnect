from django.db import models
from django.contrib.auth.models import User

gender_choices = (
    ('male', 'male'),
    ('female', 'female'),
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

class Like(models.Model):
    created_on = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Catfish(models.Model):
    created_on = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, null=False, blank=False)
    created_on = models.DateField(auto_now_add=True)