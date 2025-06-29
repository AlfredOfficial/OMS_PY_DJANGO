from django.contrib import admin
from django.utils.html import format_html
from .models import staffProfile, Department, Role, Attendance

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
    list_display = ('staff', 'date', 'time_in', 'time_out')
    search_fields = ('staff__first_name', 'staff__last_name', 'date')
    list_filter = ('staff', 'date')  

admin.site.register(staffProfile, StaffProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Attendance, AttendanceAdmin)

admin.site.site_header = "Santos College Staff Management"
admin.site.site_title = "Santos College Admin Portal"
admin.site.index_title = "Welcome to Santos College Administration"

