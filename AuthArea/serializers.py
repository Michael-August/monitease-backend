from dataclasses import fields
import email
from pyexpat import model
from rest_framework import serializers
from .models import UserModel
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=70)
    first_name = serializers.CharField(max_length=70)
    last_name = serializers.CharField(max_length=70)
    phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = UserModel
        fields = "__all__"

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

    def create(self, validated_data):
        user = UserModel.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            phone_number = validated_data['phone_number'],
            role = validated_data['role']            
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class EditUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=70)
    first_name = serializers.CharField(max_length=70)
    last_name = serializers.CharField(max_length=70)
    phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    role = serializers.CharField(max_length=20)

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'role']

class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = UserModel
        fields = ['password']

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
