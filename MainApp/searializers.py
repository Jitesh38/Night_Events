from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile,Event,RSVP,Review

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.save()
        return user
    
class UserprofileSerializer(serializers.Serializer):
    user = serializers.CharField()
    full_name = serializers.CharField()
    bio = serializers.CharField()
    location = serializers.CharField()
    
    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
        username =  validated_data['user']
        print(username)
        user = User.objects.get(username = username)
        userprofile = UserProfile(
            user = user,
            full_name = validated_data['full_name'],
            bio = validated_data['bio'],
            location = validated_data['location'],
        )
        userprofile.save()
        return userprofile
    

class EventSerializer(serializers.ModelSerializer): 
    class Meta:
       model = Event
       fields = '__all__'

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = '__all__'

                
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

        
    
    
    
       
