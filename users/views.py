from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from users.serializers import RegisterSerializer






# Create your views here.

class RegisterView(CreateAPIView):
    """
    Register view
    """
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        data['user'] = user.id
        return Response(data, status=status.HTTP_201_CREATED)

    