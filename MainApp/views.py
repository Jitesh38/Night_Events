from django.shortcuts import render,redirect,HttpResponse
from .searializers import UserSerilizer,UserprofileSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile,Event,RSVP,Review


def home(request):
    return render(request,'base.html')

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerilizer
    queryset = User.objects.all()
    
    
    
class ProfileAPI(APIView):    
    def get(self,request):
        data = UserProfile.objects.all()
        serilizer = UserprofileSerializer(data,many = True)  
        return Response(serilizer.data)