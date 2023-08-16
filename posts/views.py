from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from .models import Post
import datetime as dt
from .serializers import PostSerializer
from accounts.serializers import MemberSerializer
from accounts.models import Member
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
        
        serializer.save()
        return JsonResponse({
            'status' : 200,
            'message' : '생성 성공',
            'result' : serializer.data
        })
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse({
        #         'status' : 200,
        #         'message' : '생성 성공',
        #         'result' : serializer.data
        #     })
        # else:
        #     return JsonResponse({
        #         'status' : 400,
        #         'message' : '유효하지 않은 데이터',
        #         'result' : None
        #     })
    
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse({
            "status" : 200,
            "message" : "전체 게시글 조회 성공",
            "result" : serializer.data
        })    
class PostDetail(APIView):
    
    permission_classes = [IsWriterOrReadOnly]    
    
    def get_object(self, id):
        post = Post.objects.get(id=id)
        self.check_object_permissions(self.request, post)
        return post
    
    def get(self, request, id):
        post = self.get_object(id = id)
        serializers = PostSerializer(post)
        return JsonResponse({
            'status' : 200,
            'message' : '조회 성공',
            'result' : serializers.data
        })
    
    def put(self, request, id):
        post = self.get_object(id = id)
        serializers = PostSerializer(post, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse({
            'status' : 200,
            'message' : '수정 성공',
            'result' : serializers.data
        })
        else:
            return JsonResponse({
                'status' : 400,
                'message' : '유효하지 않은 데이터',
                'result' : None
            })
    
    def delete(self, request, id):
        post = self.get_object(id = id)
        post.delete()
        return JsonResponse({
            'status' : 200,
            'message' : '삭제 성공',
            'result' : None
        })
    
class TipPost(APIView):
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, continent):
        members = Member.objects.filter(continent=continent)
        tipList = []
        serializer = MemberSerializer(members, many=True)
        
        for member in serializer.data:
            posts = Post.objects.filter(writer=member['id'])
            serializer2 = PostSerializer(posts, many=True)
            tipList.append(serializer2.data)
            
        return JsonResponse({
            "status" : 200,
            "message" : "타이틀 조회 성공",
            "result" : tipList
        })    