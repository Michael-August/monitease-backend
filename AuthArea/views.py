from django.shortcuts import render
from AuthArea.models import UserModel
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import LoginUserSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Utils
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from django.contrib import auth

# Create your views here.

class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    name = 'Register User'

    def post(self, request):
        user_input_data = request.data
        serializer = self.serializer_class(data=user_input_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # user_data = serializer.data

        # user = UserModel.objects.get(email=user_data.email)

        # token = RefreshToken.for_user(user).access_token

        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email_verify')
        # absoluteUrl='http://' + current_site + relativeLink + "?token=" + str(token)
        # email_body = 'Hi ' + user.username + 'Use the link below to verify your email \n' + absoluteUrl
        # data = { 'email_body': email_body, 'email_to': user.email, 'email_subject': 'Verify your Email' }

        # Utils.sendEmail(data)

        # return Response(data=user_data, status=status.HTTP_201_CREATED)


# class VerifyEmailView(generics.GenericAPIView):

#     serializer_class = EmailVerificationSerializer
#     token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='For token Verification', type=openapi.TYPE_STRING)

#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.get('token')
#         try: 
#             payload = jwt.decode(token, settings.SECRET_KEY)
#             user = UserModel.objects.get(pk=payload.user_id)

#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#             return Response({'email': 'Account Succesfully activated'}, status=status.HTTP_200_OK)
#         except jwt.ExpiredSignatureError as identifier:
#             return Response({'error': 'Activation Link Expired'}, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError as identifier:
#             return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(generics.GenericAPIView):

    name = 'User Login'
    serializer_class = LoginUserSerializer
    
    def post(self, request):
        user_data = request.data
        email = user_data.get('email', '')
        password = user_data.get('password', '')

        user = auth.authenticate(username=email, password=password)
        if user:

            auth_token = jwt.encode(
                    {'email': user.email, 'role': user.role},
                    settings.JWT_SECRET_KEY 
                )

            serializer = RegisterSerializer(user)


            data = {
                'success': True,
                'message': 'User is logged in successfully',
                'user': serializer.data,
                'token': auth_token
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


