from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('signup/', views.signup_view, name = 'signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('ajax/get-roles/', views.get_roles, name='get_roles'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('timein/', views.time_in, name='timein'),
    path('timeout/', views.time_out, name='timeout'),
]