from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Librarian


class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_librarian)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsLoanOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
