from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from .models import Post
import datetime as dt
from .serializers import PostSerializer

#APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework import permissions
from config.permissions import IsWriterOrReadOnly

# Create your views here.
class PostList(APIView):
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostDetail(APIView):
    
    permission_classes = [IsWriterOrReadOnly]    
    
    def get_object(self, id):
        post = Post.objects.get(id=id)
        self.check_object_permissions(self.request, post)
        return post
    
    def get(self, request, id):
        post = self.get_object(id = id)
        serializers = PostSerializer(post)
        return Response(serializers.data)
    
    def put(self, request, id):
        post = self.get_object(id = id)
        serializers = PostSerializer(post, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        post = self.get_object(id = id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)