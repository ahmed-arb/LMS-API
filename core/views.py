from rest_framework.filters import SearchFilter
from rest_framework import viewsets

from .permissions import IsLibrarianOrReadOnly
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'author', 'publisher']
    permission_classes = [IsLibrarianOrReadOnly]
