from django.contrib import admin
from django.apps import apps
from .models import Answer,Question
# Register your models here.
class AnswerAdmin(admin.StackedInline):
    model = Answer
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]
admin.site.register(Question,QuestionAdmin)

all_teacher_models = apps.get_app_config('teacher').get_models()
for model in all_teacher_models:
    if str(model.__name__) == "Question":
        continue
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

