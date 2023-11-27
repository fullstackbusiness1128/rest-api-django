from django.shortcuts import render
from rest_framework import exceptions, status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, CommentSerializer


# Create your views here.

# user create api not permissions to all
class CustomUserCreate(APIView):
    def post(self, request):
        if request.user.role != 'S':
            raise exceptions.AuthenticationFailed(
                'You are not allowed to perform this action',
                'authorization_failed',
            )
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentCreate(APIView):
    def post(self, request):
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            return Response(comment_serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
