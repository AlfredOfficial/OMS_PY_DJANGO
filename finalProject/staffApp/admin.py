from django.contrib import admin
from .models import staffProfile, Department, Role

# Register your models here.

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'dept', 'role', 'email', 'phone', 'hire_date', 'address', 'city'
    )
    search_fields = (
        'first_name', 'last_name', 'email', 'phone', 'address', 'city'
    )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(staffProfile, StaffProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Role)
