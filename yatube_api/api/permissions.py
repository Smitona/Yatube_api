from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
import requests


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user != obj.author:
            raise PermissionDenied('Не трогайте чужое!')
        else:
            return obj.author == request.user


class GuestReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
