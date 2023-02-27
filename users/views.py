from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, Token, UntypedToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.backends import TokenBackend
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from .permission import HaveNumber
import time
from django.conf import settings



#code for the refresh token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
def home(request):
# These are the two ways of updating the value of Quizuser
#  1
    # user = QuizUser.objects.filter(user__username= 'alisher')
    # print(user[0].is_verified)
    # user.update(is_verified = True)
#  2  
    # print(user[0].is_verified)
    # user = User.objects.get(username = 'alisher')
    # print(user.quizuser.is_verified)
    # user.quizuser.is_verified = False
    # user.quizuser.save()
    # print(user.quizuser.is_verified)
    
    # str_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoidW50eXBlZCIsImV4cCI6MTY3NjY0OTY2NiwiaWF0IjoxNjc2NjQ2MDY2LCJqdGkiOiIzNDBlYmFlYTY5ODk0M2YzYTE1MDAyZmI1N2ZiM2Y0NyIsInVzZXJfaWQiOjcsInVzZXJuYW1lIjoiYWxpc2hlciJ9.6Bq5MNxaoyqKJ1iWHbTJkbfKxiOaA7u0_9UAznLniss"
    # try:
    #     token = UntypedToken.for_user(user)
    #     token.set_exp(lifetime=timedelta(hours=1))
    #     token['username'] = user.username
    #     str_token = str(token)
    #     print(str_token)
    # except Exception as e:
    #     print('Exception ========',e)   
    # # print(str_token)
    # try:
    #     decoded_token = TokenBackend(algorithm='HS256', signing_key=settings.SECRET_KEY).decode(str_token, verify=True)
    #     print( decoded_token)
    #     print(decoded_token['username'])

    # except Exception as e:
    #     print('authenticate====', e)
    
    return HttpResponse('This is the user page.')

class UserResgistration(APIView):
    def post(self, request):
        try:
            serialize = QuizUserRegisterSerializer(data = request.data)
            if serialize.is_valid():
                serialize.save()
                return Response("Resgistered Successfully Verification link is sent on you email", status=status.HTTP_201_CREATED)
            else:
                return Response(serialize.errors, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print("User Registration", e)
            return Response("The Exception raised", status= status.HTTP_400_BAD_REQUEST)
        
class UserLogin(APIView):
    def post(self, request):
        try:
            serialize = QuizUserLoginSerializer(data = request.data)
            print('before valid')
            if serialize.is_valid():
                username = serialize.data["username"]
                password = serialize.data['password']
                # Authenticating  user
                user = authenticate(username= username, password= password)
        
                #Now checking the user is authenticated and is_verified
                if user is None:
                    return Response({'Error_msg': 'The username or password is incorrect'}, status=status.HTTP_404_NOT_FOUND)
                if not(user.quizuser.is_verified):
                    return Response({'Error_msg': 'The user is not verirified'}, status=status.HTTP_403_FORBIDDEN)
                    
                tokens = get_tokens_for_user(user)
                # tokens = '123'
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('Exception in Login', e )
            return Response('Exception', status=status.HTTP_404_NOT_FOUND)
        
class UserVerification(APIView):
    def get(self, request,token):
        try:
            decoded_token = TokenBackend(algorithm='HS256', signing_key=settings.SECRET_KEY).decode(token=token, verify=True)
            username = decoded_token['username']
            user = QuizUser.objects.filter(user__username = username)
            if (user[0].is_verified):
                return Response({"msg": "The user is already Verified."})
            # This update mehtod is only work with the filter
            user.update(is_verified = True)
            return Response({"msg": "The email verified successfully."})
        except:
            return Response({"msg": " the token is invalid or expired."})

class ForgetPassword(APIView):
    def post(self, request):
        try:
            serialize = SendForgetPasswordEmail(data = request.data)
            if serialize.is_valid():
                return Response("Password reset mail is sent to your email.The mail is valid for 5 mins.", status=status.HTTP_202_ACCEPTED)
            else:
                if "system_error" in serialize.errors:
                    return Response(serialize.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(serialize.errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response('Exception', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SetForgetPassword(APIView):
    def post(self, request, token):
        try:
            decoded_token = TokenBackend(algorithm='HS256', signing_key=settings.SECRET_KEY).decode(token=token, verify=True)
            username = decoded_token['username']
            context = {"username": username}
            try:
                serialize = SetForgetPasswordWithEmail(data= request.data, context = context)
                if serialize.is_valid():
                    return Response({"msg": "Password Reset Successfully"}, status=status.HTTP_200_OK)
                else:
                    if "system_error" in serialize.errors:
                        return Response(serialize.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response('Exception', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response({"msg": " the token is invalid or expired."}, status=status.HTTP_401_UNAUTHORIZED)
        
# setting user number
class SetNumber(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        context = {"username":request.user.username}
        try:
            serialize = AddNumber(data= request.data, context = context)
            if serialize.is_valid():
                return Response({"msg": "Otp is send to your number Successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response("Excetion During in SetNumber", status= status.HTTP_500_INTERNAL_SERVER_ERROR)

# Resend Otp for verfication
class ResendOtp(APIView):
    permission_classes = [HaveNumber]
    def get(self, request):
        username = request.user.username
        quizuser = QuizUser.objects.filter(user__username = username)
        otp = random.randint(10000, 99999)
        quizuser.update(otp = otp)
        number = quizuser.number
        num = "92" +number[1:]
        message = "Your otp verification code is "+ str(otp)
        responseData = send_message(number=num, message=message)
        if responseData["messages"][0]["status"]== "0":
            return Response({"msg": "Otp is send to your number Successfully."}, status= status.HTTP_201_CREATED)
        else:
            return Response({"user_error":{responseData['messages'][0]['error-text']}}, status= status.HTTP_400_BAD_REQUEST)
        

class VerifyOtp(APIView):
    permission_classes = [HaveNumber]
    def post(self, request):
        try:
            context = {'username': request.user.username}
            print(context)
            serialize = VerifyNumberWithOtp(data = request.data, context = context)
            print('request data', request.data)
            print(serialize.is_valid())
            if serialize.is_valid():
                return Response({"msg": "Number verified successfully."}, status= status.HTTP_202_ACCEPTED)
            else:
                return Response(serialize.errors,status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('error',e)
            return Response('Exception', status= status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            