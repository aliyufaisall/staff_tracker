"""
URL configuration for pms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from portal import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    
    # New URL route specifically for handling deletions
    path('staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    # Add this path inside the urlpatterns list in pms_project/urls.py:
    path('staff/<int:staff_id>/', views.staff_profile, name='staff_profile'),
    path('assignment/delete/<int:task_id>/', views.delete_assignment, name='delete_assignment'),
    # Add this path inside the urlpatterns list in pms_project/urls.py:
    path('accounts/register/', views.register, name='register'),

]

