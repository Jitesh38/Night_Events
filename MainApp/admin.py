from django.contrib import admin
from .models import UserProfile,Event,RSVP,Review

# Register your models here.
admin.site.register((UserProfile,Event,RSVP,Review))