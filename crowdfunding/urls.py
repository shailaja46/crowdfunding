"""
URL configuration for crowdfunding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from .views import send_otp, verify_otp, register_user
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('send-otp/', send_otp),
    path('api/verify-otp/', views.verify_otp),
    path('', views.register_user, name='register'),
    path('register/', views.register_user),
    path('login/', views.login_page, name='login'),
    path('home/', views.home, name='home'),
    path('donate/', views.donate, name='donate'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('campaign_details/<int:id>/', views.campaign_details, name='campaign_details'),
    path('api/campaigns/', views.api_campaigns),
    path('api/donations/', views.api_donations),
    path('api/register/', register_user),
    path('api/', include('api.urls')), 
    path('send-otp/', send_otp), 
    path('verify-register/', views.verify_and_register),
]