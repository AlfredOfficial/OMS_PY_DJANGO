from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import staffProfile, Department, Role, Attendance, Leave

# Register your models here.
class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0 #no extra empty forms
    fields = ('date', 'time_in', 'time_out')
    readonly_fields = ('date',) # Optional: make date read-only
    can_delete = False  # Disable deletion of attendance records in the inline


class StaffProfileAdmin(admin.ModelAdmin):
    list_display = (
        'profile_image_tag',  # Show image first
        'first_name', 'last_name', 'dept', 'role', 'email', 'phone', 'hire_date', 'address', 'city'
    )
    search_fields = (
        'first_name', 'last_name', 'email', 'phone', 'address', 'city'
    )
    inlines = [AttendanceInline]

    def profile_image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:40px; height:40px; object-fit:cover; border-radius:50%;" />', obj.image.url)
        return "-"
    profile_image_tag.short_description = 'Image'

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff_user', 'staff_full_name', 'date', 'time_in_display', 'time_out_display')
    search_fields = ('staff__user__username', 'staff__first_name', 'staff__last_name', 'date')
    list_filter = ('staff', 'date')

    def staff_user(self, obj):
        return obj.staff.user.username
    staff_user.short_description = "Username"

    def staff_full_name(self, obj):
        return f"{obj.staff.first_name} {obj.staff.last_name}"
    staff_full_name.short_description = "Staff Name"  

    def time_in_display(self, obj):
        if obj.time_in:
            local_time = timezone.localtime(obj.time_in)
            return local_time.strftime('%I:%M:%S %p')
        return '-'
    time_in_display.short_description = 'Time In'

    def time_out_display(self, obj):
        if obj.time_out:
            local_time = timezone.localtime(obj.time_out)
            return local_time.strftime('%I:%M:%S %p')
        return '-'
    time_out_display.short_description = 'Time Out'

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('staff_name', 'leave_type', 'start_date', 'end_date', 'status', 'applied_at')
    search_fields = ('staff__first_name', 'staff__last_name', 'leave_type', 'status')
    list_filter = ('leave_type', 'status', 'start_date')

    def staff_name(self, obj):
        return f"{obj.staff.first_name} {obj.staff.last_name}" # Display full name of the staff not all the information. 
    staff_name.short_description = 'Staff Name'

admin.site.register(Leave, LeaveAdmin)
admin.site.register(staffProfile, StaffProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Attendance, AttendanceAdmin)

admin.site.site_header = "Santos College Staff Management"
admin.site.site_title = "Santos College Admin Portal"
admin.site.index_title = "Welcome to Santos College Administration"

