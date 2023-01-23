from rest_framework.permissions import BasePermission
from .models import Librarian


class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        is_librarian = False
        if request.user.is_authenticated:
            try:
                Librarian.objects.get(user=request.user)
                is_librarian = True
            except Librarian.DoesNotExist:
                pass

        return is_librarian
