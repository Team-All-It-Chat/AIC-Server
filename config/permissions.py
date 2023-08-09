from rest_framework import permissions

class IsWriterOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated
    # 인증된 사용자인지 여부 검증
    
    def has_object_permission(self, request, view, obj):
				
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.writer == request.user
    # 인증 받은 사용자와 게시글의 작성자가 같은지 여부 검증