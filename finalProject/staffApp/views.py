from django.utils import timezone
from datetime import time
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm, StaffProfileForm
from django.http import JsonResponse
from .models import Role, Department, staffProfile, Attendance
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from .forms import LeaveForm

 
# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES) # include request.FILES for profile picture
        profile_form = StaffProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)  # hash the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user  # link the user
            profile.is_approved = False  # set to False for admin approval
            profile.save()

            messages.success(request, 'Account created successfully! Please wait for Admin approval.')
            # return redirect('login')  # after signup
            return render(request,'staffApp/signup.html', {
                'user_form': UserForm(),
                'profile_form': StaffProfileForm(),
                'departments': Department.objects.all(),
            })
    else:
        user_form = UserForm()
        profile_form = StaffProfileForm()
    # Fetch all departments for the dropdown
    departments = Department.objects.all()    

    return render(request, 'staffApp/signup.html', {
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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            try:
                profile = staffProfile.objects.get(user=user)
                if not profile.is_approved:
                    return render(request, 'staffApp/registration/login.html', {
                        'form': form,
                        'error': 'Your account is pending for admin approval.'
                    })
            except staffProfile.DoesNotExist:
                return render(request, 'staffApp/registration/login.html', {
                    'form': form,
                    'error': 'Profile not found.'
                })
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'staffApp/registration/login.html', {
                'form': form,
                'error': 'Invalid username or password.'
            })
    else:
        form = AuthenticationForm()
    return render(request, 'staffApp/registration/login.html', {'form': form})
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #        try:
    #            profile = staffProfile.objects.get(user=user)
    #            if not profile.is_approved:
    #                return render(request, 'registration/login.html', {'error': 'Your account is pending for admin approval.'})
    #        except staffProfile.DoesNotExist:
    #            return render(request, 'registration/login.html', {'error': 'Profile not found.'})
    #        login(request, user)
    #        return redirect('dashboard')
    #     else:
           
    #         return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})
    # else:
    #     return render(request, 'registration/login.html')
    
@login_required
def dashboard(request):

    try:
        profile = staffProfile.objects.get(user=request.user) # get the profile of the logged-in user
    except staffProfile.DoesNotExist:
        messages.error(request, "Profile not found. Please contact your Administrator.") # add a message if profile not found
        return redirect('login')

    attendance_list = Attendance.objects.filter(staff=profile).order_by('-date')[:10]
    leave_form = LeaveForm()
    return render(request, 'staffApp/dashboard.html', {
        'profile': profile,
        'attendance_list': attendance_list,
        'leave_form': leave_form,
    })

@login_required
@require_POST
def time_in(request):
    profile = staffProfile.objects.get(user=request.user)
    now = timezone.localtime(timezone.now())
    today = now.date()

    # Define duty hours (example: 7:00 AM to 9:00 AM for time in)
    duty_start = time(7, 0)
    duty_end = time(9, 0)

    if not (duty_start <= now.time() <= duty_end):
        messages.error(request, "You can only Time In between 7:00 AM and 9:00 AM.")
        return redirect('dashboard')

    attendance, created = Attendance.objects.get_or_create(staff=profile, date=today)
    if attendance.time_in:
        messages.info(request, "You have already Time In today.") 
    else: 
        attendance.time_in = now
        attendance.full_clean()
        attendance.save()
        messages.success(request, "You have successfully Time In.")
    return redirect('dashboard')

@login_required
@require_POST
def time_out(request):
    profile = staffProfile.objects.get(user=request.user)
    now = timezone.localtime(timezone.now())
    today = now.date()

    # Define duty hours (example: 4:00 PM to 5:00 PM for time out)
    duty_start = time(16, 0)
    duty_end = time(17, 0)

    try:
        attendance = Attendance.objects.get(staff=profile, date=today)
        if not (duty_start <= now.time() <= duty_end):
            messages.error(request, "You can only Time Out between 4:00 PM and 5:00 PM.")
            return redirect('dashboard')
        if attendance.time_out:
            messages.info(request, "You have already Time Out today.")
        else:    
            attendance.time_out = now
            attendance.full_clean()
            attendance.save()
            messages.success(request, "You have successfully Time Out.")
    except Attendance.DoesNotExist:
        messages.error(request, "You must Time In before you can Time Out.")
    return redirect('dashboard')

@login_required
def edit_profile(request):
    profile = staffProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StaffProfileForm(instance=profile)

    return render(request, 'staffApp/edit_profile.html', {'form': form})

@login_required
def submit_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.staff = staffProfile.objects.get(user=request.user)
            leave.save()
            messages.success(request, "Leave request submitted successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Failed to submit leave request.")
            return redirect('dashboard')

def simpleui_menu(request): # wala pa ni function ang custom menu badge
    staff_count = staffProfile.objects.count()
    menu = [
        {
            'name': 'Staff profiles',
            'icon': 'fa fa-users',
            'url': '/admin/staffApp/staffprofile/',
            'badge': staff_count,  # This will show a badge with the count of
        },
    ]
    return JsonResponse(menu, safe=False)        