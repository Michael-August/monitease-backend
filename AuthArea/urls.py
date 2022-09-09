from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegisterUserView.as_view(), name='register'),
    path('register', views.RegisterUserView.as_view(), name='register'),
    # path('email_verify', views.VerifyEmailView.as_view(), name='email verify'),
    path('login', views.LoginUserView.as_view(), name='login'),
    path('<int:user_id>', views.UserDetailView.as_view(), name='Detail'),
    path('resetpassword', views.ResetPasswordView.as_view(), name='reset_password')
]
