from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm, StaffProfileForm

def signup_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = StaffProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)  # hash the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user  # link the user
            profile.save()

            return redirect('login')  # after signup
    else:
        user_form = UserForm()
        profile_form = StaffProfileForm()

    return render(request, 'signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
