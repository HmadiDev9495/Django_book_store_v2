from rest_framework import serializers
from .models import Book
import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class BookSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        print('data', data)
        if 'published_date' in data:
            data['published_date'] = datetime.datetime.strptime(data['published_date'], '%Y/%m/%d').date()
        print(data)
        result = super().to_internal_value(data=data)
        print(result)
        return result

    def validate(self, attrs):
        res = super().validate(attrs=attrs)
        return res

    def to_representation(self, instance):
        response = super().to_representation(instance=instance)
        if instance.published_date:
            response['published_date'] = instance.published_date.strftime('%Y-%m-%d')
        else:
            response['published_date'] = None
        return response

    class Meta:
        model = Book
        fields = "__all__"

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'phone_number', 'national_code')  # فیلدهای دلخواهت رو اضافه کن

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_author'] = user.is_author

        return token