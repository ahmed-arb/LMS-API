from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Librarian


class IsLibrarianOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_librarian = False
        if request.user.is_authenticated:
            try:
                Librarian.objects.get(user=request.user)
                is_librarian = True
            except Librarian.DoesNotExist:
                pass

        return bool(request.method in SAFE_METHODS or is_librarian)
