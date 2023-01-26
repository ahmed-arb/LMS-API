from django.db.models import Q
from rest_framework import serializers
from .models import Book, BookLoan, BookRequest


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

        if loan.status == "issued":
            if not loan.date_borrowed:
                raise serializers.ValidationError({"date_borrowed": "Borrow date is required when issuing a book."})
            if not loan.date_due:
                raise serializers.ValidationError({"date_due": "Due date is required when issuing a book."})

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


class BaseBookRequestSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["status"] == "rejected" and not data["reason"]:
            raise serializers.ValidationError({"reason": "Reason is required for rejected books."})

        return super().validate(data)


class FullBookRequestSerializer(BaseBookRequestSerializer):
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

    # def validate(self, data):
    #     print(data["status"])
    #     if data["status"] == "rejected" and data["reason"] == "":
    #         raise serializers.ValidationError({"reason":"Reason is required for rejected books."})

    #     return super().validate(data)
