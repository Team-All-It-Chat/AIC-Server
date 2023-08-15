from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .permissions import IsMentee
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import UpdateAPIView
from .serializers import ReviewUpdateSerializer
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from rest_framework.generics import UpdateAPIView
       
#특정 멘토의 가장 최신 리뷰 불러오기
class RecentReviewAPIView(APIView):
    def get(self, request, mentor_id):
        try:
            # mentor_id를 가진 멘토가 answerer인 Chat 중 answer가 null이 아닌 채팅 중에서 가장 최신 채팅 가져오기
            chats = Chat.objects.filter(answerer_id=mentor_id, answer__isnull=False).order_by('-id')

            for chat in chats:
                # 해당 채팅을 참조하는 리뷰 중 content가 null이 아닌 리뷰 중에서 가장 최신 리뷰 가져오기
                latest_review = Review.objects.filter(chat_id=chat.id, content__isnull=False).order_by('-id').first()
                if latest_review:
                    response_data = {
                        "status": 200,
                        "message": "멘토의 최신 리뷰 조회 성공",
                        "review": {
                            "reviewer":chat.questioner.username,
                            "review_id": latest_review.id,
                            "content": latest_review.content,
                            "sent_time": latest_review.sent_time,
                            "rate": latest_review.rate,
                        }
                    }
                    return Response(response_data)

            # mentor_id에 해당하는 채팅이 없거나 해당하는 리뷰가 없는 경우
            response_data = {
                "status": 404,
                "message": "멘토의 리뷰가 없거나 조건에 맞는 채팅이 없습니다.",
                "review": None
            }
            return Response(response_data)
            
        except Review.DoesNotExist:
            response_data = {
                "status": 405,
                "message": "멘토의 리뷰가 없습니다.",
                "review": None
            }
            return Response(response_data)

#질문 상태를 대기-> 거절으로 변경하기
class MiscellaneousAPIView(APIView):
    #permission_classes=[IsAuthenticated]
    #serializer_class = ChatUpdateStatusSerializer

    def patch(self, request,chat_id):
        chat = get_object_or_404(Chat, id=chat_id)

        if chat.answerer != request.user:
            return Response({"message": "답변자만 상태를 변경할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        chat.status = 2  # 상태를 거절로 변경
        chat.save()

        return Response({"message": "상태가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
    def get(self, request,chat_id):
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"message": "채팅이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatWithReviewSerializer(chat)
        return Response(serializer.data)
    

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
        

class ChatAPIViews(APIView):
    permission_classes = [IsAuthenticated]   
    def post(self, request):
        if not request.user.is_authenticated or request.user.is_mentor:
            return Response({"message": "이 기능을 수행하기 위해선 멘티 사용자로 로그인해야합니다."}, status=status.HTTP_401_UNAUTHORIZED)

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
            
            chat.status = 1
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
    

