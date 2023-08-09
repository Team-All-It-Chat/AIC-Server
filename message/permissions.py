from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from rest_framework import permissions

class IsMentee(BasePermission):
    def has_permission(self, request, view):
        # 로그인한 사용자가 멘토인 경우 접근을 허용하지 않음
        if request.user.is_authenticated and request.user.is_mento:
            return False
        # 그 외에는 접근을 허용함
        return True

class IsNonMentorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_mentor

class IsAnswerer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.answerer == request.user

class IsQuestioner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.questioner == request.user
