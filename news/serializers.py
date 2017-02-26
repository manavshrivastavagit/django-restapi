from rest_framework import serializers

from news.models import News, Comment

from students.serializers import StudentAuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    posted_by = StudentAuthorSerializer(read_only=True)
    content = serializers.CharField(max_length=2048)

    class Meta:
        model = Comment
        fields = (
            'id',
            'posted_by', 'content',
            'posted_on',
            'edited', 'last_edited_on'
        )
        depth = 1


    def create(self, validated_data):
        news = self.context['news']
        request = self.context['request']

        posted_by = request.user.student

        return Comment.objects.create(
            news=news, posted_by=posted_by, **validated_data
        )

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class CommentReadSerializer(CommentSerializer):
    posted_by = StudentAuthorSerializer(read_only=True)


class NewsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=100)
    content = serializers.CharField(min_length=5, max_length=10000)
    author = StudentAuthorSerializer(read_only=True)
    comment_set = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = (
            'id',
            'title', 'content',
            'posted_on', 'author',
            'comment_set',
            'edited', 'last_edited_on'
        )
        depth = 2


    def create(self, validated_data):
        request = self.context['request']
        author = request.user.student

        return News.objects.create(author=author, **validated_data)

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance