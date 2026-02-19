from rest_framework import serializers
from .models import Book, ImageBook
import datetime


class ImageBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBook
        fields = ['id', 'image', 'name']


class BookSerializer(serializers.ModelSerializer):
    images = ImageBookSerializer(many=True, read_only=True)
    publisher_name = serializers.CharField(source='publisher.username', read_only=True)
    publisher = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'name', 'author', 'publisher', 'publisher_name',
            'published_date', 'price', 'currency', 'category',
            'page_count', 'publisher_name', 'description', 'is_published',
            'images', 'created_at'
        ]
        read_only_fields = ['publisher']


class BookCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            'name', 'author', 'published_date', 'price', 'currency',
            'category', 'page_count', 'description', 'is_published'
        ]


class BookUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            'name', 'author', 'published_date', 'price', 'currency',
            'category', 'page_count', 'description', 'is_published'
        ]


class ImageBookUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageBook
        fields = ['image', 'name']