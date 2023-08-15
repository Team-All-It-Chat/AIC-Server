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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatSerializer, ReviewSerializer
from .models import Chat, Review
from django.shortcuts import get_object_or_404

class ChatAPIViews(APIView):
     #질문 등록하기
    def post(self, request, format=None):
        # 질문과 관련된 데이터를 받아옴
        question = request.data.get('question')
        answerer = request.data.get('answerer')

        if not question or not answerer:
            return Response({"message": "question과 answerer 필드를 제공해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 질문 데이터를 직렬화
        serializer = ChatSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # 질문 데이터 저장
            chat = serializer.save()

            # 해당 질문에 대한 리뷰 생성
            Review.objects.create(chat=chat)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #답변 등록하기
    def patch(self,request,*args,**kwargs):
        chat_id = request.data.get('chat_id')  # JSON 데이터에서 chat_id 받아오기
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"message": "질문이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        if chat.answerer != request.user:
            return Response({"message": "질문자만 답변을 업데이트할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        # 답변과 이미지 업로드 처리
        serializer = self.get_serializer(chat, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    #채팅 전체 내용 보기
    def get(self, request, format=None):
        user = request.user

        # 현재 로그인한 사용자가 질문자인 모든 채팅을 불러옴
        questioner_chats = Chat.objects.filter(questioner=user)

        # 현재 로그인한 사용자가 답변자인 모든 채팅을 불러옴
        answerer_chats = Chat.objects.filter(answerer=user)

        # 두 쿼리셋을 합쳐서 사용자와 관련된 모든 채팅을 불러옴
        my_chats = questioner_chats | answerer_chats

        serializer = ChatSerializer(my_chats, many=True)
        return Response(serializer.data)
    #후기 등록하기
    def put(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"message": "질문이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        try:
            review = Review.objects.get(chat_id=chat_id)
        except Review.DoesNotExist:
            return Response({"message": "리뷰가 존재하지 않습니다."}, status=status.HTTP_405_NOT_FOUND)

        serializer = self.get_serializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        chat.status = 2
        chat.save()
        return Response(serializer.data)   

#질문 상태를 대기-> 수락으로 변경하기
class ChatUpdateStatusAPIView(UpdateAPIView):
    queryset = Chat.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = ChatUpdateStatusSerializer

    def update(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"message": "질문이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        if chat.answerer != request.user:
            return Response({"message": "답변자만 상태를 변경할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        chat.status = 1  # status를 1로 변경
        chat.save()

        return Response({"message": "상태가 변경되었습니다."}, status=status.HTTP_200_OK)



#가장 최신의 질문글 불러오기
class RecentQuestionAPIView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        # 현재 로그인한 사용자가 questioner인 채팅들 중 가장 최근에 생성된 채팅을 가져옴
        recent_chat = Chat.objects.filter(questioner=user).order_by('-question_time').first()

        if recent_chat:
            serializer = ChatSerializer(recent_chat)
            return Response(serializer.data)
        else:
            return Response({"message": "최근에 올린 질문글이 없습니다."}, status=401)
        
        
        
        
        
        
        
        
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
