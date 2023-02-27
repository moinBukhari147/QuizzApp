from django.contrib import admin
from .models import QuizUser
# Register your models here.

@admin.register(QuizUser)
class QuizUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_student', 'is_verified']
    

