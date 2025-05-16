from django import forms 
from django.contrib.auth.models import User
from .models import staffProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class StaffProfileForm(forms.ModelForm):
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = staffProfile
        exclude = ['user', 'salary', 'bonus'] 