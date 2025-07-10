from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime
import datetime

class Department(models.Model):
    name = models.CharField(max_length=100, null = False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100, null = False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True) # ForeignKey to Department

    def __str__(self):
        return self.name

class staffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    first_name = models.CharField(max_length=100, null = False)
    last_name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, default=0)
    hire_date = models.DateField()
    email = models.EmailField(max_length=100, null = False)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False) # for admin approval
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg', null=True, blank=True)

    def __str__(self):
        return "%s %s %s %s %s %s %s" %(
            self.first_name, self.last_name, self.dept, self.role, self.email, self.address, self.city
        )
    
    # not yet done
class Attendance(models.Model):
    staff = models.ForeignKey(staffProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s %s %s %s" %(
            self.staff, self.date, self.time_in, self.time_out
        )

    def is_late(self):
        if self.time_in:
            local_time = localtime(self.time_in).time()
            return local_time > datetime.time(8, 0)
        # if self.time_in and self.time_in.time() > datetime.time(8, 0):
        #     return True
        return False        

class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('SICK', 'Sick Leave'),
        ('VACATION', 'Vacation Leave'),
        ('EMERGENCY', 'Emergency Leave'),
        ('OTHERS', 'Others'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    staff = models.ForeignKey(staffProfile, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff} - {self.leave_type} ({self.start_date} to {self.end_date})"