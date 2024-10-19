from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerilizer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    
    def validate(self, data):                
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('username is already taken')
        return data
        
    def create(self , data):
        user = User.objects.create_user(username=data['username'],password=data['password'])
        user.save()
        return data
    
    
class UserprofileSerializer(serializers.ModelSerializer):
       
    class Meta:
        model = UserProfile
        depth = 1
        fields = '__all__'
    
