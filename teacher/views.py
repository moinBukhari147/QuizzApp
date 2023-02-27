from django.shortcuts import render, HttpResponse
from django.http import request
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from users.permission import IsTeacher

# Appyly Authentication and apply the logic of @loginrequired, I think this can done with the authetication only
# Add the error code like 404 in the responses

# Create your views here.
def test(request):
    return HttpResponse('This is the teacher Api Home')



class question(APIView):
    permission_classes = [IsTeacher]
    def get(self, request, format = None):
    
        all_question = Question.objects.all()
        try:
                serializer = QuestionSerializer(all_question, many = True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response('Error in class Question in get method during serialization')
    def post(self, request, format = None):
        try:
            serializer = QuestionSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error_msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Question post error", e)
            return Response('Exception raised from Questin class, post request', status=status.HTTP_400_BAD_REQUEST)

