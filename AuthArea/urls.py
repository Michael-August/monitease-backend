from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterUserView.as_view(), name='register'),
    # path('email_verify', views.VerifyEmailView.as_view(), name='email verify'),
    path('login', views.LoginUserView.as_view(), name='login')
]
