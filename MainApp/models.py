from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300,default='')
    bio = models.TextField(default='')
    location = models.CharField(max_length=150,default='')
    # profile_picture = models.ImageField(upload_to='profile_picture/')
    
    def __str__(self):
        return self.user.username
    
    
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,default='')
    description = models.TextField(default='')
    organizer = models.CharField(max_length=500,default='')
    location = models.CharField(max_length=150,default='')
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(default=now)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.title
    
class RSVP(models.Model):
    STATUS_CHOICES = [
        ('Going','Going'),
        ('Maybe','Maybe'),
        ('Not Going','Not Going')
    ]
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES)
    
    
    def __str__(self):
        return self.user.username + " : " + self.status

class Review(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.CharField(max_length=300,default='')
    
    
    def __str__(self):
        return self.event.title + " by " + self.user.username
    
    