from django import forms 
from django.contrib.auth.models import User
from .models import staffProfile, Attendance
import datetime

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class StaffProfileForm(forms.ModelForm):
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = staffProfile
        exclude = ['user', 'salary', 'bonus', 'email', 'is_approved'] 

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['time_in', 'time_out']

    def clean(self):
        cleaned_data = super().clean()
        time_in = cleaned_data.get('time_in')
        time_out = cleaned_data.get('time_out')

        min_time_in = datetime.time(8, 0)
        min_time_out = datetime.time(16, 0)

        if time_in and time_in.time() < min_time_in:
            raise forms.ValidationError("You can only time in at or after 8:00 AM.")

        if time_out and time_out.time() < min_time_out:
            raise forms.ValidationError("You can only time out at or after 4:00 PM.")

        return cleaned_data



# wala pa na fix ang late fo time in okkkkk
#still figuring out how to do it