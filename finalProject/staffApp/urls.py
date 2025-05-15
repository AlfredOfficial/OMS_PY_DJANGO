from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name = 'signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]