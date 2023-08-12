from django.db import models
from django.conf import settings
from accounts.models import *



class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    questioner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name="질문자",related_name='chat_as_questioner')
    answerer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name="답변자",related_name='chat_as_answerer' )
    question = models.TextField(max_length=300)
    answer = models.TextField(max_length=2000,blank=True, null=True)
    question_time = models.DateTimeField(blank=True, null=True)
    answer_time = models.DateTimeField(blank=True, null=True)
    status=models.IntegerField(default=0)

#'질문 대기'=0,'답변 완료'=1,'거절'=2

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id=models.OneToOneField(Chat,on_delete=models.CASCADE)
    content = models.TextField(max_length=500,blank=True, null=True)
    sent_time = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    rate = models.IntegerField(default=0,blank=True, null=True)