from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
  
  
  
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email', 'password1', 'password2']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'ethnicity','gender', 'location', 'profile_photo','preference', 'bio']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email'] 


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'ethnicity','gender', 'location', 'profile_photo','preference', 'bio']