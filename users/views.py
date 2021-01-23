import json

from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from users import news
from users.models import Hackathon, Profile
from users.permissions import IsOwnerOrReadOnly
from users.serializers import HackathonSerializer, ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    ProfileDetail shows user profile and requires authentication
    if a post request 
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user__username'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


@api_view(['GET'])
def api_root(request, format=None):
    """
    api_root displays api in an html webpage
    """

    return Response({
        'profiles': reverse('profile-list', request=request, format=format)
    })


@api_view(['GET'])
def index(request):
    """default root directory will show news as json"""

    data = news.show_news(news.DEFAULT_NEWS)
    return Response(data=data)


@api_view(['GET'])
def profile_news(request, username):
    """get current user's prefered news source as json"""

    # get user's profile
    user = get_object_or_404(User.objects.all(), username=username)
    profile = Profile.objects.get(user=user)
    
    # get news as json
    data = news.show_news(profile.news_pref)
    return Response(data=data)


class HackathonViewset(viewsets.ModelViewSet):
    """many to many relationship
    https://medium.com/@kingsleytorlowei/building-a-many-to-many-modelled-rest-api-with-django-rest-framework-d41f54fe372
    """
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
