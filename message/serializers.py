from rest_framework import serializers
from .models import Chat,Review


class ChatUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'



class ChatSerializer(serializers.ModelSerializer):
    questioner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Chat
        fields = '__all__'
    def create(self, validated_data):
        questioner = self.context['request'].user
        validated_data['questioner'] = questioner
        chat = Chat.objects.create(**validated_data)
        return chat

class AllChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        
class ChatAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ChatWithReviewSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'question', 'answer', 'question_time', 'answer_time', 'status', 'reviews']

    def get_reviews(self, chat):
        reviews = Review.objects.filter(chat_id=chat.id)
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

