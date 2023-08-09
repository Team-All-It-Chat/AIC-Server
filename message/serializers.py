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

