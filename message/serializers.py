from rest_framework import serializers
from .models import Chat,Review

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


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

       
class ChatAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


from accounts.models import *

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class ChatWithReviewSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Chat
        fields = '__all__'
    def get_reviews(self, chat):
        reviews = Review.objects.filter(chat_id=chat.id)
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

class AllChatSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    questioner = MemberSerializer()
    answerer = MemberSerializer()

    class Meta:
        model = Chat
        fields = '__all__'
        
    def get_reviews(self, chat):
        reviews = Review.objects.filter(chat_id=chat.id)
        serializer = ReviewSerializer(reviews, many=True)
        
        for review in serializer.data:
            questioner = Member.objects.get(id=chat.questioner.id)
            answerer = Member.objects.get(id=chat.answerer.id)
            review['questioner'] = {
                'id': questioner.id,
                'name': questioner.name,
                'profile':questioner.profile
            }
            review['answerer'] = {
                'id': answerer.id,
                'name': answerer.name,
                'profile':answerer.profile
            }
        
        return serializer.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['questioner'] = {
            'id': instance.questioner.id,
            'name': instance.questioner.name,
            'profile':instance.questioner.profile
        }
        data['answerer'] = {
            'id': instance.answerer.id,
            'name': instance.answerer.name,
            'profile':instance.answerer.profile
        }
        return data