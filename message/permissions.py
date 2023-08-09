from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User


class IsMentee(BasePermission):
    def has_permission(self, request, view):
        # 로그인한 사용자가 멘토인 경우 접근을 허용하지 않음
        if request.user.is_authenticated and request.user.is_mento:
            return False
        # 그 외에는 접근을 허용함
        return True



# #receiver 확인이 잘 안됨...

# class IsReceiver(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_authenticated and obj.question.receiver == request.user



# class IsAnswerReceiver(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_authenticated and obj.answer.receiver == request.user