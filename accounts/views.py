from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import *
from django.core.mail import EmailMessage
import random

class MemberProfile(APIView):
    def get(self, request, id):
        profiles = get_object_or_404(Member, id=id)
        serializer = MemberSerializer(profiles)
        
        return JsonResponse({
            "data" : serializer.data,
            "status" : 200
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
            
            # 6자리 인증번호 생성
            MENTEE_CERT_NUMBER = ""
            MENTOR_CERT_NUMBER = ""

            for _ in range(6):
                MENTEE_CERT_NUMBER += str(random.randrange(0,10))
            
            # 이메일로 인증번호 발송
            subject = "All-It-Chat 멘티 가입 인증번호"
            to = [serializer.data['kor_email']]
            message = MENTEE_CERT_NUMBER
            EmailMessage(subject=subject, body=message, to=to).send()

            if serializer.data['foregin_email'] != '':
                
                for _ in range(6):
                    MENTOR_CERT_NUMBER += str(random.randrange(0,10))

                # 이메일로 인증번호 발송
                subject = "All-It-Chat 멘토 가입 인증번호"
                to = [serializer.data['foreign_email']]
                message = MENTOR_CERT_NUMBER
                EmailMessage(subject=subject, body=message, to=to).send()
            
            res = Response(
                {
                    "member":serializer.data,
                    "message":"register success",
                    "token":{
                        "access_token":access_token,
                        "refresh_token":refresh_token,
                    },
                    "cert_number" : {
                        "mentee" : MENTEE_CERT_NUMBER,
                        "mentor" : MENTOR_CERT_NUMBER,
                        },
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthView(APIView):
    serializer_class = AuthSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
						
        if serializer.is_valid(raise_exception=False):
            member = serializer.validated_data['member']
            access_token = serializer.validated_data['access_token']
            refresh_token = serializer.validated_data['refresh_token']
            res = Response(
                {
                    "member": member,
                    "message":"login success",
                    "token":{
                        "access_token":access_token,
                        "refresh_token":refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request):
        res = Response({
		    "message":"logout success"
	    }, status=status.HTTP_202_ACCEPTED)
		
		# cookie에서 token 값들을 제거함
        res.delete_cookie("access-token")
        res.delete_cookie("refresh-token")
        return res

class ConfirmView(APIView):
    def post(self, request):
        
        member = get_object_or_404(Member, name=request.data["member"]["name"])
        print(member.is_active)
        
        if not request.data["confirm"]:
            return JsonResponse({
            "message" : "실패"
            })
        elif member.is_active:
            member.is_mento = True
            member.save()
            return JsonResponse({
                "message" : "멘토 인증 성공"
            })
        else:        
            member.is_active = True
            member.save()
            return JsonResponse({
                "message" : "멘티 인증 성공"
            })
        
    
        
        