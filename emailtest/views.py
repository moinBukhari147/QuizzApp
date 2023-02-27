from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
import requests
import json

# Create your views here.
def home(request):
    return HttpResponse('This is the home of Email test')

def send_email(request):
    with get_connection(
        host = settings.EMAIL_HOST,
        port = settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:
        subject = 'This is the first test email'
        email_from = settings.EMAIL_HOST_USER
        recipient = ['oinbukhari14777778990@gmail.com']
        message = "Hi Moin how are you. This is my fist message."
        sent = EmailMessage(subject, message, email_from, recipient, connection=connection).send()
        print(sent)
    
    url = "https://api.zerobounce.net/v2/validate"  
    email = 'oinbukhaewewri1477777899099@gmail.com'
    apikey = 'd2051c2a052b41bdbe69eadd0319c4c2'
    params = {"email": email, "api_key": apikey}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        response = json.loads(r.content)
        print(response)
        if 'error' in response:
            print('Emailchecker is full')
        elif response['status']=='valid':
            print('email exist')
        else:
            print('email doesnot exist')
    
    return HttpResponse ('The email send')