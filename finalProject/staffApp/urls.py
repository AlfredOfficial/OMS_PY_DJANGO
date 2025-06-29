from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('signup/', views.signup_view, name = 'signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('ajax/get-roles/', views.get_roles, name='get_roles'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('timein/', views.time_in, name='timein'),
    path('timeout/', views.time_out, name='timeout'),
    # password reset URLS pero not sure if they are working!
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]