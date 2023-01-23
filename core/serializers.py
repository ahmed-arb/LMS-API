from rest_framework import serializers
from .models import Book, BookLoan


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'cover', 'author', 'publisher', 'stock']


class FullBookLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan
        fields = ['id', 'user', 'book', 'status', 'created_at', 'date_borrowed', 'date_due', 'date_returned']
        read_only_fields = ('user', 'created_at')


class BasicBookLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan
        fields = ['id', 'user', 'book', 'status', 'created_at', 'date_borrowed', 'date_due', 'date_returned']
        read_only_fields = ('user', 'status', 'created_at', 'date_borrowed', 'date_due', 'date_returned')
