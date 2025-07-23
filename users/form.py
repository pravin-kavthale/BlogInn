from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']  # Removed fullname and summary (they don't belong here)


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['image', 'gender', 'age', 'fullname', 'summary']
