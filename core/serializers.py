from django.db.models import Q
from rest_framework import serializers
from .models import Book, BookLoan


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "name", "cover", "author", "publisher", "stock"]


class BaseBookLoanSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.filter(~Q(stock=0)))

    def validate(self, attrs):
        loan = BookLoan(**attrs)
        book = Book.objects.get(pk=loan.book.id)

        # requested book should be available
        if book.stock == 0:
            raise serializers.ValidationError("Requested book is out of stock.")

        return super().validate(attrs)


class FullBookLoanSerializer(BaseBookLoanSerializer):
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
