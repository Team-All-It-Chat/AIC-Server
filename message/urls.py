from django.urls import path
from .views import *

urlpatterns = [
     path('',ChatAPIViews.as_view()),
     path('detail/',ChatWithReviewAPIView.as_view()),
     path('status/',ChatUpdateStatusAPIView.as_view()),
     path('recent/',RecentQuestionAPIView.as_view())
    ]
