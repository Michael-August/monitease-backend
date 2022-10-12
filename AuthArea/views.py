from datetime import datetime, timedelta
import random
from django.shortcuts import render, get_object_or_404
from AuthArea.backends_auth import JWTAuthentication
from AuthArea.models import UserModel
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import EditUserSerializer, LoginUserSerializer, RegisterSerializer, ResetPasswordSerializer
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
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    name = 'Register User'
    queryset = UserModel.objects.all()

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

    def get(self, request):
        users = UserModel.objects.all().order_by('-created_at')

        serializer = self.serializer_class(instance=users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserDetailView(generics.GenericAPIView):
    serializer_class = EditUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, user_id):
        user = get_object_or_404(UserModel, pk=user_id)
        serializer = self.serializer_class(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        try:
            data = request.data
            user = get_object_or_404(UserModel, pk=user_id)

            serializer = self.serializer_class(data=data, instance=user)

            if serializer.is_valid():
                serializer.save()
                userSerializer = RegisterSerializer(user)

                return Response(data=userSerializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        try:
            if request.user.role != 'DIRECTOR' and request.user.role != 'ADMIN':
                response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(data=response, status=status.HTTP_403_FORBIDDEN)

            user = get_object_or_404(UserModel, pk=user_id)

            user.delete()
            response = {
                'success': True,
                'status_code': status.HTTP_204_NO_CONTENT,
                'message': 'User deleted successfully'
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Check your request and try again'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request):
        try:
            user = UserModel.objects.filter(email=request.user.email)

            if not user:
                response = {
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User not found, check email and try again'
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                user.password = user.set_password(request.data.get('password'))
                user.save()
                response = {
                        'success': True,
                        'status_code': status.HTTP_200_OK,
                        'message': 'Password reseted successfully',
                    }
                
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Check your request and try again' + str(e)
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)



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

            # random_number = Random.randint(self, a=1, b=10000)
            # print(random_number)

            auth_token = jwt.encode(
                    {"exp": datetime.now() + timedelta(days=1), 'email': user.email, 'role': user.role, 'random': random.randint(0, 1000)},
                    settings.JWT_SECRET_KEY 
                )

            serializer = RegisterSerializer(user)
            user.last_login = datetime.now()


            data = {
                'success': True,
                'message': 'User is logged in successfully',
                'user': serializer.data,
                'token': auth_token
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


