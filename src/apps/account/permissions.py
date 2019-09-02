from rest_framework import permissions
from rest_framework_jwt.utils import jwt_decode_handler


class IsAuthenticatedWechat(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.META.get("HTTP_AUTHORIZATION")

        if not token:
            return False
        user = jwt_decode_handler(token)
        request.auth = user
        return True
