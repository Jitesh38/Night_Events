from django.shortcuts import render
from .searializers import *
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


def home(request):
    return render(request,'base.html')

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerilizer
    queryset = User.objects.all()    
    
    
class ProfileAPI(APIView):    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        data = UserProfile.objects.all()
        serilizer = UserprofileSerializer(data,many = True)  
        return Response(serilizer.data)
    
    def post(self,request):
        data = request.data
        serializer = UserprofileSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status" : "True" , "message" : "User Created Successfully"},status.HTTP_201_CREATED)
        return Response({"Status" : "False" , "error" : serializer.errors},status.HTTP_400_BAD_REQUEST)
    

class EventAPI(APIView):   
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    
    def get(self,request,slug=0):
        if slug == 0:
            data = Event.objects.all()
            # Pagination
            page = request.GET.get('page' , 1)
            page_size = 3
            paginator = Paginator(data,page_size)
            print(paginator.page(page))
            serializer = EventSerializer(paginator.page(page) , many = True)
            return Response(serializer.data,status.HTTP_200_OK)
        else:
            data = Event.objects.get(id = slug)
            serializer = EventSerializer(data)
            return Response(serializer.data,status.HTTP_200_OK)
        
    def post(self,request):
        data = request.data
        serializer = EventSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status" : "True" , "message" : "Event added Successfully"},status.HTTP_201_CREATED)
        return Response({"Status" : "False" , "error" : serializer.errors},status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,slug):
        event = Event.objects.get(id = slug)
        serializer = EventSerializer(event,data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response({"Status" : "True" , "message" : "Event updated Successfully"},status.HTTP_201_CREATED)
        return Response({"Status" : "False" , "error" : serializer.errors},status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,slug):
        event = Event.objects.get(id = slug)
        event.delete()
        return Response({"Status" : "True" , "message" : "Event deleted Successfully"},status.HTTP_200_OK)
    

class RSVPAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
        
    def get(self,request,id):
        event = Event.objects.get(id = id)
        data = RSVP.objects.filter(event = event)
        serializer = RSVPSerializer(data,many = True)
        return Response(serializer.data,status.HTTP_200_OK)    
    
    def post(self,request,id):
        event = Event.objects.get(id = id)
        serializer = RSVPSerializer(data = request.data)
        if serializer.is_valid():
            rsvp = RSVP(event = event,user=request.user,status = request.data['status'])
            rsvp.save()
            return Response({"Status" : "True" , "message" : "RSVP added Successfully"},status.HTTP_201_CREATED)
        return Response({"status":"False","error":serializer.errors},status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET','PUT'])

def rsvp_apiview(request,eid,uid):
        
    if request.method == 'PUT':
        event = Event.objects.get(id = eid)
        user = User.objects.get(id = uid)
        rsvp = RSVP.objects.get(event = event,user = user)        
        serializer = RSVPSerializer(rsvp,data = request.data,partial = True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)         
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)    
    else :
        event = Event.objects.get(id = eid)
        user = User.objects.get(id = uid)
        rsvp = RSVP.objects.get(event = event,user = user)        
        serializer = RSVPSerializer(rsvp)
        return Response(serializer.data,status.HTTP_201_CREATED)      
        

class ReviewAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id):
        event = Event.objects.get(id = id)
        data = Review.objects.filter(event = event)
        serializer = ReviewSerializer(data,many = True)
        return Response(serializer.data)    
    
    def post(self,request,id):
        event = Event.objects.get(id = id)
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            review = Review(event = event,user=request.user,rating = request.data['rating'],comment = request.data['comment'])
            review.save()
            return Response({"Status" : "True" , "message" : "RSVP added Successfully"},status.HTTP_201_CREATED)
        return Response({"status":"False"})      
    
    
class LoginAPI(APIView):
        
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username = username,password = password)
            
            if user is None:
                pass
            else:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
                
            
            
        