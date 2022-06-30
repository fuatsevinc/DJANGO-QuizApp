from django.shortcuts import render
from quiz.models import Quiz

from quiz.serializers import QuizSerializer
from rest_framework import viewsets

# Create your views here.


class QuizMVS(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer