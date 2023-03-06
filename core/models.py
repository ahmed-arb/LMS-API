"""Core model schemas"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Override base User model"""

    class UserGender(models.IntegerChoices):
        """Enumeration class for user gender"""

        MALE = 0, _("Male")
        FEMALE = 1, _("Female")
        OTHER = 2, _("Other")

    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.SmallIntegerField(choices=UserGender.choices, blank=True, null=True)
    books = models.ManyToManyField("Book", through="BookLoan")

    @property
    def is_librarian(self):
        """checks is the user is librarian or not

        Returns:
            Bool: if the user is librarian.
        """
        return self.groups.filter(name='librarian').exists()



class Book(models.Model):
    """
    Books in the lms are represented by this model.

    All fields are required. Stock means the number of books available in the library.
    """

    name = models.CharField(max_length=100)
    cover = models.URLField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    stock = models.IntegerField()

    def __str__(self):
        return str(self.name)



class BookLoan(models.Model):
    """This model represents user book loans. Loans are managed by librarians and admins."""

    class BookLoanStatus(models.IntegerChoices):
        """Enumeration class for book loans statues"""

        REQUESTED = 0, _("Requested")
        ISSUED = 1, _("Issued")
        REJECTED = 2, _("Rejected")
        RETURNED = 3, _("Returned")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    status = models.SmallIntegerField(
        choices=BookLoanStatus.choices, default=BookLoanStatus.REQUESTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    date_borrowed = models.DateField(null=True, blank=True)
    date_due = models.DateField(null=True, blank=True)
    date_returned = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.name}"


class BookRequest(models.Model):
    """This model represents unavailable books requested by users"""

    class BookRequestStatus(models.IntegerChoices):
        """Enumeration class for book request statues"""

        PENDING = (0, "Pending")
        APPROVED = (1, "Approved")
        REJECTED = (2, "Rejected")

    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='book_requests')
    book_name = models.CharField(max_length=100)
    status = models.SmallIntegerField(
        choices=BookRequestStatus.choices,
        default=BookRequestStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book_name}"
