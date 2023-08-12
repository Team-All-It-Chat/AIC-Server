from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view()), 
    path('<str:continent>/', TipPost.as_view()),
]