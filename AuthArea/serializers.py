from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import UserModel
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=70)
    first_name = serializers.CharField(max_length=70)
    last_name = serializers.CharField(max_length=70)
    phone_number = serializers.IntegerField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'phone_number', 'password', 'first_name', 'last_name']

    def validate(self, attrs):
        username_exists = UserModel.objects.filter(username=attrs['username']).exists()

        if username_exists:
            raise serializers.ValidationError(detail="User with this username already exist")

        email_exists = UserModel.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise serializers.ValidationError(detail="User with this email already exist")

        phone_number_exists = UserModel.objects.filter(phone_number=attrs['phone_number']).exists()

        if phone_number_exists:
            raise serializers.ValidationError(detail="User with this phone number already exist")

        return super().validate(attrs)



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=777)

    class Meta:
        model = UserModel
        fields = ['token']


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=40)
    password = serializers.CharField(min_length=8)

    class Meta:
        model = UserModel
        fields = ['email', 'password']
