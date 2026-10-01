# api/urls.py
from django.contrib import admin
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, DonationViewSet, register_user

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)
router.register(r'donations', DonationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include(router.urls)),
    path('register/', register_user),
     path('verify-register/', views.verify_and_register),
    path('', views.home),
]    
