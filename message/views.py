from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .permissions import IsMentee
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from rest_framework.generics import UpdateAPIView

#질문 상태를 대기-> 수락으로 변경하기
class ChatUpdateStatusAPIView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class = ChatUpdateStatusSerializer

    def patch(self, request):
        chat_id = request.data.get('chat_id')

        chat = get_object_or_404(Chat, id=chat_id)

        if chat.answerer != request.user:
            return Response({"message": "답변자만 상태를 변경할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        chat.status = 1  # 상태를 1로 변경
        chat.save()

        return Response({"message": "상태가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)

#가장 최신의 질문글 불러오기
class RecentQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        # 현재 로그인한 사용자가 questioner인 채팅들 중 가장 최근에 생성된 채팅을 가져옴
        recent_chat = Chat.objects.filter(questioner=user).order_by('-question_time').first()

        # 현재 로그인한 사용자가 questioner 또는 answerer인 채팅들 중 가장 최근에 생성된 채팅을 가져옴
        recent_chat = Chat.objects.filter(Q(questioner=user) | Q(answerer=user)).order_by('-question_time').first()
        
        if recent_chat:
            serializer = ChatSerializer(recent_chat)
            return Response(serializer.data)
        else:
            return Response({"message": "최근에 올린 질문글이 없습니다."}, status=401)
        

class ChatWithReviewAPIView(APIView):
    def get(self, request):
        chat_id = request.data.get('chat_id')  # JSON 형식으로 chat_id 받음
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"message": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatWithReviewSerializer(chat)
        return Response(serializer.data)


class ChatAPIViews(APIView):
    permission_classes = [IsAuthenticated]   
    def post(self, request):
        if not request.user.is_authenticated or request.user.is_mentor:
            return Response({"message": "You need to be logged in as a non-mentor user to perform this action."}, status=status.HTTP_401_UNAUTHORIZED)

        questioner = request.user
        serializer = ChatSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(questioner=questioner, question_time=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        chat_id = request.data.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id, answerer=request.user)
        serializer = ChatAnswerSerializer(chat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(answer_time=timezone.now())

            if chat.questioner.chat_count is not None:
                chat.questioner.chat_count += 1
            else:
                chat.questioner.chat_count=1
            
            chat.questioner.save()
            
            if chat.answerer.chat_count is not None:
                chat.answerer.chat_count += 1
            else:
                chat.answerer.chat_count=1
            
            chat.answerer.save()
            
            chat.status = 2
            chat.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        chat_id = request.data.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id, questioner=request.user)
        rate = request.data.get('rate')
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sent_time=timezone.now())
                      
            if chat.answerer.review_count is not None:
                chat.answerer.review_count += 1
            else:
                chat.answerer.review_count=1
            
            chat.answerer.save()
                       
            if chat.answerer.total_score is None:
                chat.answerer.total_score = rate
            else:
                chat.answerer.total_score = (float(chat.answerer.total_score)*float(chat.answerer.review_count-1)+float(rate))/float(chat.answerer.review_count)

            chat.answerer.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #채팅 전체 내용 보기
    def get(self, request, format=None):
        user = request.user

        # 현재 로그인한 사용자가 질문자인 모든 채팅을 불러옴
        questioner_chats = Chat.objects.filter(questioner=user)

        # 현재 로그인한 사용자가 답변자인 모든 채팅을 불러옴
        answerer_chats = Chat.objects.filter(answerer=user)

        # 두 쿼리셋을 합쳐서 사용자와 관련된 모든 채팅을 불러옴
        my_chats = questioner_chats | answerer_chats

        serializer = AllChatSerializer(my_chats, many=True)
        return Response(serializer.data)
    
    

