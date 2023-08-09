from django.urls import path
from .views import *

urlpatterns = [
    #path('create-question/', QuestionCreateView.as_view(), name='create_question'),
    path('q/',QuestionCreateView.as_view()),
    path('qq/',question.as_view()),
    
    path('',MyAPIViews.as_view()),
    path('status/',ChatUpdateStatusAPIView.as_view()),
    path('recent/',RecentQuestionAPIView.as_view())
    ]
