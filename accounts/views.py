from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request)

        return Response(serializer.data)