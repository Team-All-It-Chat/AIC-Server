from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # 회원가입/로그인/로그아웃
    path('signup/', RegisterView.as_view()),
    path('login/mentee/', MenteeAuthView.as_view()),
    path('login/mentor/', MentorAuthView.as_view()),
    # 프로필
    path('<str:continent>/', MentorProfile.as_view()),
    # 토큰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]