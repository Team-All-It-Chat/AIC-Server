from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
from .serializers import *
from .permissions import IsMentee
from rest_framework.permissions import IsAuthenticated


class ChatCreateAPIView(APIView):
    permission_classes=[IsMentee,IsAuthenticated]
    def post(self, request, format=None):
        serializer = ChatSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # chat_instance = serializer.instance
            # chat_instance.status = 1
            # chat_instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import ChatUpdateSerializer

class ChatUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Chat.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChatUpdateSerializer

    def update(self, request, *args, **kwargs):
        chat = self.get_object()
        if chat.questioner != request.user:
            return Response({"message": "질문자만 답변을 업데이트할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 답변과 이미지 업로드 처리
        serializer = self.get_serializer(chat, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Review
from .serializers import ReviewUpdateSerializer

class ReviewUpdateAPIView(UpdateAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewUpdateSerializer

    def update(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"message": "질문이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        try:
            review = Review.objects.get(chat_id=chat_id)
        except Review.DoesNotExist:
            return Response({"message": "리뷰가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
     
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import ChatUpdateStatusSerializer

class ChatUpdateStatusAPIView(UpdateAPIView):
    queryset = Chat.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChatUpdateStatusSerializer

    def update(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"message": "질문이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        if chat.questioner != request.user:
            return Response({"message": "질문자만 상태를 변경할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        chat.status = 1  # status를 1로 변경
        chat.save()

        return Response({"message": "상태가 변경되었습니다."}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import ChatSerializer

class MyChatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import ChatSerializer

class RecentQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        # 현재 로그인한 사용자가 questioner인 채팅들 중 가장 최근에 생성된 채팅을 가져옴
        recent_chat = Chat.objects.filter(questioner=user).order_by('-question_time').first()

        if recent_chat:
            serializer = ChatSerializer(recent_chat)
            return Response(serializer.data)
        else:
            return Response({"message": "최근에 올린 질문글이 없습니다."}, status=204)
