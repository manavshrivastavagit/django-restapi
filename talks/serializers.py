from rest_framework import serializers

from students.serializers import UserInfoSerializer
from .models import Meetup, Talk


class TalkSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)
    topic = serializers.CharField(required=True, max_length=500)
    description = serializers.CharField(required=True, max_length=10000)
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Talk
        fields = ('id', 'author', 'topic', 'description', 'video_url', 'votes_count') 

    def get_votes_count(self, obj):
        return obj.votes.count()

    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        
        meetup = self.context['meetup']

        return Talk.objects.create(meetup=meetup, author=author, **validated_data)


class MeetupSerializer(serializers.ModelSerializer):
    talks = TalkSerializer(many=True, read_only=True)

    class Meta:
        model = Meetup
        fields = ('id', 'date', 'talks')
