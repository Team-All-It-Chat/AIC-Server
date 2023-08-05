from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # 프로필
    path('', MemberProfile.as_view()),
    # 회원가입/로그인/로그아웃
    path('join/', RegisterView.as_view()),
    path('login/', AuthView.as_view()),
    # 토큰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 이메일
    path('join/<str:result>', EmailView.as_view()),
]