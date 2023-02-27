from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='userhome'),
    path('register', views.UserResgistration.as_view(), name = 'userRegistration'),
    path('login', views.UserLogin.as_view(), name='userlogin'),
    path('verify-email/<token>', views.UserVerification.as_view(), name="verify-email"),
    path('forget-password', views.ForgetPassword.as_view(), name='forget-password'),
    path('set-forget-password/<token>', views.SetForgetPassword.as_view(), name="set-forget-password"),
    path('set-number', views.SetNumber.as_view(), name= "setNumber"),
    path('resend-otp', views.ResendOtp.as_view(), name= 'resendOtp'),
    path('verify-otp', views.VerifyOtp.as_view(), name= "verifyOtp"),
]