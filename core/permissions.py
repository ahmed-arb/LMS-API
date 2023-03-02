"""
Core permission classes
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsLibrarian(BasePermission):
    """
    Allows access to only librarians
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_librarian)


class ReadOnly(BasePermission):
    """
    Allows access to read-only requests
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwner(BasePermission):
    """
    Allows access only to owners
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
