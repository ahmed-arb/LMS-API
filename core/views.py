from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated

from .permissions import IsLibrarian
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'author', 'publisher']

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            permission_classes = [IsAuthenticated, IsLibrarian]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
