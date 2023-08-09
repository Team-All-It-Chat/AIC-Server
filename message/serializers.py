from rest_framework import serializers
from .models import Chat,Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

from rest_framework import serializers
from .models import Chat

class ChatUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['status']


class ChatSerializer(serializers.ModelSerializer):
    question_time = serializers.DateTimeField(read_only=True)
    answer = serializers.CharField(read_only=True)
    image=serializers.ImageField()
    answer_time = serializers.DateTimeField(required=False, allow_null=True)
    class Meta:
        model = Chat
        fields = '__all__'

    def create(self, validated_data):
        # 현재 로그인한 사용자 가져오기
        questioner = self.context['request'].user
        print(questioner)
        # "질문자" 필드를 현재 로그인한 사용자로 설정
        validated_data['questioner'] = questioner
        

        # 현재 시간을 설정하여 question_time에 저장
        validated_data['question_time'] = timezone.now()

        # Chat 인스턴스 생성
        chat = Chat.objects.create(**validated_data)

        # Review 인스턴스 생성 (null 값으로)
        Review.objects.create(chat_id=chat, content=None, rate=None, sent_time=None)

        return chat

import boto3
from botocore.exceptions import ClientError
from config.settings import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

# VALID_IMAGE_EXTENSIONS = [ "jpg", "jpeg", "png", "gif", ]


from rest_framework import serializers
from .models import Chat
from django.utils import timezone

class ChatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
      
    # def validate(self, data): 
    #     image = data.get('image')

    #     if not image.name.split('.')[-1].lower() in VALID_IMAGE_EXTENSIONS:
    #         raise serializers.ValidationError("Not an Image File")

    #     return data

    def update(self, instance, validated_data):
        # 이미지를 S3 버킷으로 바로 업로드하기 위해 이미지 처리 추가
        # image_file = validated_data.get('image')
        # if image_file:
        #     s3 = boto3.client('s3',
        #         aws_access_key_id = AWS_ACCESS_KEY_ID,
        #         aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        #         region_name = AWS_REGION)
        #     try:
        #         s3.upload_fileobj(image_file, AWS_STORAGE_BUCKET_NAME, image_file.name)  # 파일 업로드
        #         img_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{image_file.name}"
        #         instance.image = img_url
        #     except:
        #         raise serializers.ValidationError("Invalid Image File")

        # answer_time 자동 설정
        instance.answer_time = timezone.now()

        # 답변 업데이트 처리
        instance.answer = validated_data.get('answer', instance.answer)

        # status를 2로 변경
        instance.status = 2

        instance.save()
        return instance


from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        
from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

