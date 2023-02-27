from django.http import request
from django.shortcuts import render, HttpResponse
from teacher.models import Question

def home(request):
    # class A():
    #     def pr():
    #         print('Moin')
    # categoty = {"name":'moins'}
    # categoty['name']= A()
    # print(categoty['name'])
    
    a = Question.objects.all()[0]
    print(a.get_ans)
    return HttpResponse('This is the home page')
