"""
Core app serializers
"""
from django.db.models import Q
from rest_framework import serializers

from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)

from .models import Book, BookLoan, BookRequest


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    User Create serializer. Adds user profile fields when creating a user.
    """

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "username", "password", "email", "phone_number", "gender"]


class CurrentUserSerializer(BaseUserSerializer):
    """
    Current User serializer. Adds user profile fields when getting a user.
    """

    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "email", "phone_number", "gender", "is_librarian"]


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Books
    """

    class Meta:
        model = Book
        fields = ["id", "name", "cover", "author", "publisher", "stock"]


class BaseBookLoanSerializer(serializers.ModelSerializer):
    """
    Base serializer for book loans. It makes sure:

    * All book loans only have available books for loan.
    * Issued books have: date_borrowed and date_due.
    * Returned books have date_returned.
    """
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.exclude(stock=0))
    # book = BookSerializer()
    # book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.exclude(stock=0), write_only=True)

    def validate(self, attrs):
        loan = BookLoan(**attrs)
        book = Book.objects.get(pk=loan.book.id)

        # requested book should be available
        if book.stock == 0:
            raise serializers.ValidationError("Requested book is out of stock.")

        if loan.status == "issued":
            if not loan.date_borrowed:
                raise serializers.ValidationError(
                    {"date_borrowed": "Borrow date is required when issuing a book."}
                )
            if not loan.date_due:
                raise serializers.ValidationError(
                    {"date_due": "Due date is required when issuing a book."}
                )

        if loan.status == "returned" and not loan.date_returned:
            raise serializers.ValidationError(
                {"date_returned": "Returned date is required when returning a book."}
            )

        return super().validate(attrs)


class ReadBookLoanSerializer(BaseBookLoanSerializer):
    book = BookSerializer()
    class Meta:
        model = BookLoan
        fields = [
            "id",
            "user",
            "book",
            "status",
            "created_at",
            "date_borrowed",
            "date_due",
            "date_returned",
        ]
class FullBookLoanSerializer(BaseBookLoanSerializer):
    """
    Book loans serializer for librarians and admin.
    """

    class Meta:
        model = BookLoan
        fields = [
            "id",
            "user",
            "book",
            "status",
            "created_at",
            "date_borrowed",
            "date_due",
            "date_returned",
        ]
        read_only_fields = ("user", "created_at")


class UserBookLoanSerializer(BaseBookLoanSerializer):
    """
    Book Loan serializer for users.
    """

    class Meta:
        model = BookLoan
        fields = [
            "id",
            "user",
            "book",
            "status",
            "created_at",
            "date_borrowed",
            "date_due",
            "date_returned",
        ]
        read_only_fields = (
            "user",
            "status",
            "created_at",
            "date_borrowed",
            "date_due",
            "date_returned",
        )


class BaseBookRequestSerializer(serializers.ModelSerializer):
    """
    Base book request serializer from which all book request serializers must inherit. It makes sure that:

    * Admins and librarian provide reason for rejecting a book request.

    """

    def validate(self, attrs):
        if attrs.get("status", None) == "rejected" and not attrs.get("reason", None):
            raise serializers.ValidationError(
                {"reason": "Reason is required for rejected books."}
            )

        return super().validate(attrs)


class FullBookRequestSerializer(BaseBookRequestSerializer):
    """
    Book request serializer for admins and librarians.
    """

    class Meta:
        model = BookRequest
        fields = [
            "id",
            "user",
            "book_name",
            "status",
            "created_at",
            "reason",
        ]
        read_only_fields = ("id", "user", "created_at")


class UserBookRequestSerializer(BaseBookRequestSerializer):
    """
    Book request serializer for Users.
    """

    class Meta:
        model = BookRequest
        fields = [
            "id",
            "user",
            "book_name",
            "status",
            "created_at",
            "reason",
        ]
        read_only_fields = (
            "id",
            "user",
            "status",
            "created_at",
            "reason",
        )
