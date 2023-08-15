from django.urls import path
from .views import *

urlpatterns = [
     path('',ChatAPIViews.as_view()),
     path('<int:chat_id>/',MiscellaneousAPIView.as_view()),
     path('recent/',RecentQuestionAPIView.as_view()),
     path('recent/<int:mentor_id>/',RecentReviewAPIView.as_view())
    ]