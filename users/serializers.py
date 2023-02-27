from rest_framework import serializers
from .models import QuizUser, User
from django.contrib.auth import authenticate
import requests
import json
from rest_framework_simplejwt.tokens import UntypedToken
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import random
import vonage

def send_message(message, number):
    client = vonage.Client(key="5e478de7", secret="4FF39reDSP5Ph6Qo")
    sms = vonage.Sms(client)
    responseData = sms.send_message(
    {
        "from": "QuizzApp",
        "to": number,
        "text": message
    }
    )
    return responseData




def send_verify_email(link, email):
    with get_connection(
        host = settings.EMAIL_HOST,
        port = settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:
        subject = 'QuizzApp Email Verification '
        email_from = settings.EMAIL_HOST_USER
        recipient = [email]
        message = f"Click on the link given bellow to verify you email address. \n {link}"
        EmailMessage(subject, message, email_from, recipient, connection=connection).send()
        return
        

#Register User
class QuizUserRegisterSerializer(serializers.ModelSerializer):
    f_name = serializers.CharField(max_length = 255, write_only = True)
    l_name = serializers.CharField(max_length = 255)
    email = serializers.EmailField()
    username = serializers.CharField(max_length = 255)
    password = serializers.CharField(max_length = 255)
    password2 = serializers.CharField(max_length = 255)
    class Meta:
        model = QuizUser
        fields = ['f_name','l_name','email','username','password','password2', 'is_student']
    #using the api of zerobounce and check if the email is exist or not.
    @staticmethod    
    def is_validEmail(email):
        url = "https://api.zerobounce.net/v2/validate"  
        apikey = '01df0bf0fd4441b8a1e2640cd793a5b5'
        params = {"email": email, "api_key": apikey}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            response = json.loads(r.content)
            if 'error' in response:
                return 'error'
            elif response['status']=='valid':
                return "valid"
            else:
                return 'invalid'
        
        
    def validate(self, validated_data):
        if (validated_data['password']!=validated_data['password2']):
            raise serializers.ValidationError({'user_error': 'password and confirm password are not same.'})
        if (User.objects.filter(email = validated_data['email'].lower()).exists()):
            raise serializers.ValidationError({'user_error': 'The email is already exist.'})
        if(User.objects.filter(username = validated_data['username'].lower()).exists()):
            raise serializers.ValidationError({'user_error': 'The username is already exist.'})
        #calling the function to check the validity of the email.
        # valid_email = self.is_validEmail(validated_data['email'])
        # if(valid_email == 'error'):
        #     raise serializers.ValidationError('The email validator limit is reached.')
        # if(valid_email== 'invalid'):
        #     raise serializers.ValidationError('The email is invalid. Enter a valid email')
        
        # creating the user for QuizUser profile
        user = User.objects.create_user(first_name = validated_data['f_name'], 
                                        last_name = validated_data['l_name'],
                                        email=validated_data['email'],
                                        username=validated_data['username'],
                                        password=validated_data['password']
                                        )
        user.save()
        
        # Creating Token for the user verification
        try:
            token = UntypedToken.for_user(user)
            token.set_exp(lifetime=timedelta(hours=1))
            token['username'] = user.username
            str_token = str(token)
        except Exception as e:
            # if exception raised --- delete the user created and raise the error.
            user.delete()
            raise serializers.ValidationError({'system_error': 'There is error of generating token while registering the token. The error is from server side.'})
        
        # Sending mail for the user verification
        try:
            link = f"http://127.0.0.1:8000/user/verify-email/{str_token}"
            send_verify_email(link=link, email=user.email)
        except Exception as e:
            raise serializers.ValidationError({"system_error": "There is error while sending email user not created. The error is from server side "})
            
        is_student = validated_data['is_student']
        validated_data = {"user":user, "is_student": is_student}
        return validated_data

        
    def create(self, validated_data):
        return QuizUser.objects.create(**validated_data)

    
class QuizUserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 255)
    password = serializers.CharField(max_length = 255)
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def validate(self, attrs):
        # if the user wanted to login with the number
        error = None
        try:
            number = attrs['username']
            num = int(number)
            # Checking the user with the followng number is exist and the number is verified
            quizuser = QuizUser.objects.filter(number = number).first()
            if quizuser is None:
                error = ({"user_error": "The User with the following number does not exist."})
                raise Exception
            elif not quizuser.number_verified:
                
                error = ({"user_error": "The Number is not verified."})
                raise Exception
            attrs['username'] = quizuser.user.username
            
        except:
            # As the validation error cannot be raised inside the try box, because it will jump to except when validationError is raise so
            if error is not None:
                raise serializers.ValidationError(error)
            if('@' in attrs['username']):
                try:
                    #if email Checking the email exits if yes return its username
                    attrs['username'] = User.objects.filter(email = attrs['username']).values('username').first()["username"]
                    
                except:
                    raise serializers.ValidationError({'user_error': 'The email does not exist.'})
            else:
                #  if username cheking the user exist
                username = attrs['username']
                if not(User.objects.filter(username = username).exists()):
                    raise serializers.ValidationError({'user_error': 'The username does not exist.'})
        return attrs
            
        
class SendForgetPasswordEmail(serializers.ModelSerializer):
    email = serializers.CharField(max_length = 255)
    class Meta:
        model = User
        fields = ['email']
    def validate_email(self, email):
        if('@' in email):
            user = User.objects.filter(email = email).first()
            if user is None:
                raise serializers.ValidationError({'user_error': 'The email does not exist. Enter a valid email'})

        else:
            #  if username cheking the user exist
            user = User.objects.filter(username = email).first()
            if user is None:
                raise serializers.ValidationError({'user_error': 'The username does not exist. Enter the valid username.'})
        # create token of the user for passwrd reset
        try:
            token = UntypedToken.for_user(user=user)
            token.set_exp(lifetime=timedelta(minutes=5))
            token['username'] = user.username
            str_token = str(token)
        except Exception as e:
            raise serializers.ValidationError({"system_error": "There is error from server side while creating token for password reset."})
        # Sending email for the password reset.
        try:
            link = f"http://127.0.0.1:8000/user/set-forget-password/{str_token}"
            send_verify_email(email=user.email, link=link)
        except Exception as e:
            raise serializers.ValidationError({'system_error': 'There is an error from the server side while sending the email for Password rest.'})
            
        return email
    
class SetForgetPasswordWithEmail(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length = 255, write_only = True)
    class Meta:
        model = User
        fields = ['password', 'password2']
    def validate(self, attrs):
        if attrs['password']!=attrs['password2']:
            return serializers.ValidationError({"user_error": "Password and Confirm Password are not same."})
        
        user = User.objects.filter(username = self.context.get('username')).first()
        # it cannot be possible that user not found but it's an extra layer of check.
        if user is None:
            raise serializers.ValidationError({"system_error": "The user not found"})
        user.set_password(attrs['password'])
        user.save()
        return attrs
# serialzier for adding the number for user.
class AddNumber(serializers.ModelSerializer):
    number = serializers.CharField(max_length = 11)
    class Meta:
        model = QuizUser
        fields = ['number']
    def validate(self, attrs):
        # Checking the number is valid or not
        try:
            num = int(attrs['number'])
        except:
            raise serializers.ValidationError({"user_error": "The Number is not valid."})
        
        username = self.context.get('username')
        # Checking that does this number is taken by Other user.
        anotherUser = User.objects.filter(quizuser__number = attrs['number']).first()
        if(anotherUser is not None):
            # it is possible that the user is again generating this request for otp with this same number.
            if (anotherUser.username !=username):
                raise serializers.ValidationError({"user_error": "This number is already taken by another user."})
        # setting number
        quizuser = QuizUser.objects.filter(user__username = username)
        quizuser.update(number = attrs['number'], number_verified = False)
        
        # generating otp
        otp = random.randint(10000, 99999)
        quizuser.update(otp = otp)
        # Sending message
        message = "Your otp verfication code is" + str(otp)
        num = num%10000000000
        responseData = send_message(message=message, number="92"+ str(num))
        if responseData["messages"][0]["status"] != "0":
            raise serializers.ValidationError({"user_error":{responseData['messages'][0]['error-text']}})
        return attrs
# verfying the numver with otp
class VerifyNumberWithOtp(serializers.ModelSerializer):
    otp = serializers.CharField(max_length = 5)
    class Meta:
        model = QuizUser
        fields = ['otp','number']
    def validate(self, attrs):
        username = self.context.get('username')
        quizuser = QuizUser.objects.filter(user__username = username)

        if attrs["otp"]!= quizuser[0].otp:
            raise serializers.ValidationError({"user_error": "Invalid otp."})
        quizuser.update(otp = "0", number_verified = True)

        return attrs
    