from django.contrib import admin

# Register your models here.
# api/admin.py
from django.contrib import admin
from .models import Campaign, Donation

admin.site.register(Campaign)
admin.site.register(Donation)
