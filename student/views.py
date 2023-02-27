from django.http import HttpResponse,request
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from .models import Record
from teacher.models import Question,Subject
from teacher.serializers import QuestionSerializer
from django_filters.rest_framework import FilterSet
from django_filters import rest_framework as filters
from rest_framework import exceptions
from rest_framework import status
from users.permission import IsStudent

# Create your views here.
def home(request):
    return HttpResponse('This is the home of the student page')

# Now I need to create the forign key realiton of user student with the Record and then save the record with that user creadetials.
# For the above I also need add the authentication that only the authenticated user can submit result, check result, 


# The user can also filter their result according to the subject i.e only english or math 
class RecordFilter(FilterSet):
    
    subject = filters.CharFilter(lookup_expr = 'icontains')
    class Meta:
        model = Record
        fields = ['subject']


class result(APIView):
    permission_classes = [IsStudent]
    
    def get(self, request, format =None, pk = None):
        if pk is None:
            all_results = Record.objects.all()
            all_results = RecordFilter(request.GET, queryset = all_results)
            serialize = RecordSerializer(all_results.qs, many = True)
            return Response(serialize.data, status= status.HTTP_200_OK)
    def post(self, request, format = None, pk = None):
        if 'paper' not in request.data:
            raise exceptions.ValidationError({'paper':'This field is required and should be in lower case.'})
        if 'subject' not in request.data:
            raise exceptions.ValidationError({'subject':'This field is required and should be in lower case.'})
        paper = request.data['paper']
        total_marks = 0
        obtained_marks = 0
        for question in paper:
            try:          
                correct_ans, marks = Question.objects.filter(uid = question['uid']).values_list('correct_ans', 'marks').first()
                total_marks = total_marks + marks
                if correct_ans.lower() == question['ans'].lower():
                    obtained_marks= obtained_marks+ marks
            except Exception as e:
                return Response({"error_msg": f"question with the uid {question['uid']} doest not exist. There is an error while getting the uid."},
                                status=status.HTTP_404_NOT_FOUND)
        sub_result = {
            "subject": request.data['subject'].lower(),
            "score": obtained_marks,
            "result_status": True if (obtained_marks/total_marks*100)>50 else False
        }
        try:
            serialize = RecordSerializer(data= sub_result)
            if serialize.is_valid():
                serialize.save()
                return Response(serialize.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response('exception raised in result class post function', status=status.HTTP_400_BAD_REQUEST)
    
class TestQuestion(APIView):
    permission_classes = [IsStudent]
    def get(self, request, pk = None):
        if pk is None:
            return Response("The Subject should be provided e.g 'url../student/test/english'", status=status.HTTP_400_BAD_REQUEST)
        else:
            pk = pk.lower()
            subjec = Subject.objects.filter(subject_name = pk).first()
            if subjec:
                all_question = subjec.subject_quest.all()
                try:
                    serializer = QuestionSerializer(all_question, many = True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response('Error in class TestQuestion in get method during Serialization', status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("The subject is not exists.", status=status.HTTP_404_NOT_FOUND)
        
