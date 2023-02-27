
from django.urls import path, include
from . import views 
urlpatterns = [
    path("", views.test, name = "Testing page"),
    path("question/", views.question.as_view(), name="question"),
]
