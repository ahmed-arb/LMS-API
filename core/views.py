from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from templated_mail.mail import BaseEmailMessage

from .permissions import IsLibrarian, ReadOnly
from .models import Book, BookLoan
from .serializers import FullBookLoanSerializer, UserBookLoanSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "author", "publisher"]
    permission_classes = [IsAdminUser | IsLibrarian | ReadOnly]


class BookLoanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_fields = ["book", "user", "status"]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_librarian:
            return BookLoan.objects.all()

        return BookLoan.objects.filter(user_id=user.id)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_librarian:
            return FullBookLoanSerializer
        return UserBookLoanSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], permission_classes=[IsAdminUser | IsLibrarian])
    def remind(self, request, pk):
        loan = BookLoan.objects.get(pk=pk)
        message = BaseEmailMessage(
            template_name="emails/overdue_books.html",
            context={
                "name": loan.user,
                "book": loan.book,
            },
        )
        message.send([loan.user.email])
        return Response({"detail": "reminder email sent to user"})
