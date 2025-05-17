from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm, StaffProfileForm
from django.http import JsonResponse
from .models import Role, Department, staffProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
 
# Create your views here.
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
    # Fetch all departments for the dropdown
    departments = Department.objects.all()    

    return render(request, 'signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'departments': departments,
    })

def get_roles(request):
    department_id = request.GET.get('department_id')
    roles = Role.objects.filter(department_id=department_id).values('id', 'name')
    return JsonResponse(list(roles), safe = False)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard') #redirect to dashboard after login
        else:
            #invalid login 
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
@login_required
def dashboard(request):
    profile = staffProfile.objects.get(user=request.user)
    return render(request, 'dashboard.html', {'profile': profile})        