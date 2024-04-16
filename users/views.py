from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# user login view
class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)
    
# user logout view
class UserLogoutAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
        else:
            return Response({"message": "User not logged in."}, status=400)
            
        return Response({"message": "User logged out successfully."}, status=204)
    
# retrieve user info view
class UserInfoAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user_data = {
                "username": request.user.username,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone_number": request.user.phone_number,
                "weight": request.user.weight,
                "height": request.user.height,
                "body_part": request.user.body_part,
            }
            return Response(user_data, status=200)
        else:
            return Response({"message": "User not logged in."}, status=400)
