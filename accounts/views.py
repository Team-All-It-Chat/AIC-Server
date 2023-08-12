from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import *
from django.core.mail import EmailMessage

class MentorProfile(APIView):
    def get(self, request, continent):
        profiles = Member.objects.filter(continent=continent)
        serializer = MemberSerializer(profiles, many=True)
        
        return JsonResponse({
            "status" : 200,
            "message": "멘토 프로필 조회 성공",
            "result" : serializer.data
        })
        

class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            member = serializer.save(request)
            token = RefreshToken.for_user(member)
            refresh_token = str(token)
            access_token = str(token.access_token)
            
            # refresh token 저장
            member.refresh_token = refresh_token
            member.save()
            
            res = Response(
                {
                    "member":serializer.data,
                    "message":"register success",
                    "token":{
                        "access_token":access_token,
                        "refresh_token":refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenteeAuthView(APIView):
    serializer_class = AuthSerializer

    def post(self, request):

        data = {
            "username" : "Jouning",
            "password" : "eyljKFRI636="
        }
        
        serializer = self.serializer_class(data=data)
						
        if serializer.is_valid(raise_exception=False):
            member = serializer.validated_data['member']
            access_token = serializer.validated_data['access_token']
            refresh_token = serializer.validated_data['refresh_token']
            res = Response(
                {
                    "status" : 200,
                    "message":"멘티 로그인 성공",
                    "member": member,
                    "token":{
                        "access_token":access_token,
                        "refresh_token":refresh_token,
                    },
                }
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
        else:
            return JsonResponse({
            "status" : 400,
            "message" : "멘티 로그인 실패",
            "result" : None
        })
        
    
    def delete(self, request):
        res = JsonResponse({
            "status" : 200,
		    "message":"멘티 로그 아웃 성공",
            "result" : None
	    })
		
		# cookie에서 token 값들을 제거함
        res.delete_cookie("access-token")
        res.delete_cookie("refresh-token")
        return res
    
class MentorAuthView(APIView):
    serializer_class = AuthSerializer

    def post(self, request):

        data = {
            "username" : "Ibberson",
            "password" : "xehcJNTP117="
        }
        
        serializer = self.serializer_class(data=data)
						
        if serializer.is_valid(raise_exception=False):
            member = serializer.validated_data['member']
            access_token = serializer.validated_data['access_token']
            refresh_token = serializer.validated_data['refresh_token']
            res = Response(
                {
                    "status" : 200,
                    "message":"멘토 로그인 성공",
                    "member": member,
                    "token":{
                        "access_token":access_token,
                        "refresh_token":refresh_token,
                    },
                }
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
        else:
            return JsonResponse({
            "status" : 400,
            "message" : "멘토 로그인 실패",
            "result" : None
        })
    
    def delete(self, request):
        res = JsonResponse({
            "status" : 200,
		    "message":"멘토 로그 아웃 성공",
            "result" : None
	    })
		
		# cookie에서 token 값들을 제거함
        res.delete_cookie("access-token")
        res.delete_cookie("refresh-token")
        return res
          
        
        