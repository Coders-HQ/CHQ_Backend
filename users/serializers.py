from rest_framework import serializers
from users.models import Profile, Hackathon
from django.contrib.auth.models import User


class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-date']
        model = Hackathon
        fields = [
            'date',
            'location',
            'members',
            'website',
            'title',
            'id'
        ]
        extra_kwargs = {'members': {'required': False}}

class ProfileSerializer(serializers.ModelSerializer):
    """for projects you can use list seperator if more than one"""
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    hackathons = HackathonSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'github_url',
            'bio',
            'username',
            'first_name',
            'last_name',
            'email',
            'mobile_score',
            'devops_score',
            'front_end_score',
            'back_end_score',
            'database_score',
            'languages',
            'cv',
            'academic_qualification',
            'academic_qualification_file',
            'projects',
            'hackathons',
            'news_pref',
            'github_score'
        ]
        extra_kwargs = {'hackathons': {'required': False}}
        read_only_fields = ['github_score']

