from rest_framework import serializers
from.models import *

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer']
    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

class subjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["subject_name"]
        
    def validate_subject_name(self, value):
        all_sub = list(Subject.objects.values_list('subject_name'))
        if value.lower() in all_sub:
            raise serializers.ValidationError({"Error_msg": 'The category is already exist.'})
        return value
    
    def create(self, validated_data):
        return Subject.objects.create(**validated_data)

class QuestionSerializer(serializers.ModelSerializer):
    # options = serializers.ListField(write_only = True)
    
    options = AnswerSerializer(write_only = True, many = True)    
    subjectCat = serializers.CharField(max_length = 255, write_only = True)
    ans = serializers.ReadOnlyField(source = "get_ans")
    
    # Method no 2 of getting the  asnwers of the each question
    # ans = serializers.SerializerMethodField() 
    
    class Meta:
        model = Question        
        fields = ['uid','marks', 'question','subjectCat', 'correct_ans', 'ans', 'options']
        extra_kwargs = {
                        "correct_ans":{"write_only":True},
                        "uid":{"read_only":True}}
        
    # defination of Method 2 getting asnwers of the each questiion
    # def get_ans(self, obj):
    #     AllAns = list(obj.question_ans.all())
    #     print("ans obj",AllAns)
    #     answers = [anss.answer for anss in AllAns]
    #     random.shuffle(answers)
    #     return answers
    
    def validate_subjectCat(self, value):
        value = value.lower()
        if not(Subject.objects.filter(subject_name = value).exists()):
            obj = Subject.objects.create(subject_name = value)
            obj.save()
        else:
            obj = Subject.objects.get(subject_name = value)
        return obj
    
    def validate_question(self, value):
        value = value.lower()
        if Question.objects.filter(question = value).exists():
            raise serializers.ValidationError("This question is already exist")
        return value
    
    def create(self, validated_data):        
        validated_data['subject']= validated_data.pop('subjectCat')
        options = validated_data.pop('options')
        obj = Question.objects.create(**validated_data)
        try:
            serialize = AnswerSerializer(data = options, many = True)
            if serialize.is_valid():
                serialize.save(question = obj)
            else:
                obj.delete()
                raise serializers.ValidationError(serialize.errors)
        except Exception as e:
            obj.delete()
            raise serializers.ValidationError("Exception the anser is not created, error in QuestinSerialzer create method.")
        return obj
        