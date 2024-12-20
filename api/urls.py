"""
URL configuration for Night_Events project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from MainApp import views
from MainApp.views import UserViewSet,ProfileAPI,EventAPI,RSVPAPI,ReviewAPI,rsvp_apiview,LoginAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
urlpatterns = router.urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('',include(router.urls)),
    path('login/',LoginAPI.as_view()),
    path('userprofile/',ProfileAPI.as_view()), 
    path('events/',EventAPI.as_view()),
    path('events/<int:slug>/',EventAPI.as_view()),
    path('events/<int:id>/rsvp/',RSVPAPI.as_view()),
    path('events/<int:eid>/rsvp/<int:uid>/',rsvp_apiview),
    path('events/<int:id>/review/',ReviewAPI.as_view()),
     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
