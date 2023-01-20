from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    books = models.ManyToManyField('Book', through='BookLoan', related_name='users')


class Book(models.Model):
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='books/')
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    stock = models.IntegerField()

    def __str__(self):
        return self.name


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class BookLoan(models.Model):
    class BookLoanStatus(models.TextChoices):
        REQUESTED = 'requested', _('Requested')
        ISSUED = 'issued', _('Issued')
        REJECTED = 'rejected', _('Rejected')
        RETURNED = 'returned', _('Returned')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=BookLoanStatus.choices, default=BookLoanStatus.REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    date_borrowed = models.DateField(null=True, blank=True)
    date_due = models.DateField(null=True, blank=True)
    date_returned = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.book.name}'


class BookRequest(models.Model):
    class BookRequestStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=BookRequestStatus.choices, default=BookRequestStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.book_name}'
