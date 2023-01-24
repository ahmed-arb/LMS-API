from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .permissions import IsLibrarian, IsLoanOwner, ReadOnly
from .models import Book, BookLoan
from .serializers import FullBookLoanSerializer, UserBookLoanSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "author", "publisher"]
    permission_classes = [IsAdminUser | IsLibrarian | ReadOnly]


class BookLoanViewSet(viewsets.ModelViewSet):
    queryset = BookLoan.objects.all()
    permission_classes = [IsAdminUser | IsLibrarian | IsLoanOwner | ReadOnly]
    filterset_fields = ["book", "user", "status"]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_librarian:
            return BookLoan.objects.all()

        return BookLoan.objects.filter(user_id=user.id)

    def get_serializer_class(self):
        if self.request.user.is_librarian:
            return FullBookLoanSerializer
        return UserBookLoanSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
