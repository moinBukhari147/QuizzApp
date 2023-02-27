
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path("test/<pk>", views.TestQuestion.as_view(), name="question"),
    path("test", views.TestQuestion.as_view(), name="question"),
    path('result', views.result.as_view(), name='result')
    
]
