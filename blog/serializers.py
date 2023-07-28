from .models import Blog
from rest_framework import serializers
from users.serializers import UserSerializer


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'publication_date', 'author']


class BlogListSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'publication_date', 'author']
