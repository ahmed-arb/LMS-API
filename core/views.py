"""
Views for core app
"""

from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from templated_mail.mail import BaseEmailMessage

from .permissions import IsLibrarian
from .models import Book, BookLoan, BookRequest
from .serializers import (
    FullBookLoanSerializer,
    FullBookRequestSerializer,
    UserBookLoanSerializer,
    BookSerializer,
    UserBookRequestSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    """
    Book viewset
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "author", "publisher"]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class BookLoanViewSet(viewsets.ModelViewSet):
    """
    Book loan viewset. It only lists users own loans or all loans for admins and librarians.
    """

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

    @action(
        detail=True, methods=["get"], permission_classes=[IsAdminUser | IsLibrarian]
    )
    def remind(self, request, pk):
        """
        Reminds user, by email, for their outstanding loan.

        Args:
            request: Request object
            pk: primary key for BookLoan

        Returns:
            dict: detail message
        """
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


class BookRequestViewSet(viewsets.ModelViewSet):
    """
    Book request model viewset for requesting unavailable books.
    """

    permission_classes = [IsAuthenticated]
    filterset_fields = ["user", "status"]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_librarian:
            return BookRequest.objects.all()

        return BookRequest.objects.filter(user_id=user.id)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_librarian:
            return FullBookRequestSerializer
        return UserBookRequestSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
