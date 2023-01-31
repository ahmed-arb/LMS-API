"""Core model schemas"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Override base User model"""

    class UserGender(models.TextChoices):
        """Enumeration class for user gender"""

        MALE = "m", _("Male")
        FEMALE = "f", _("Female")
        OTHER = "other", _("Other")

    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=20, choices=UserGender.choices, blank=True)
    books = models.ManyToManyField("Book", through="BookLoan", related_name="users")

    @property
    def is_librarian(self):
        """checks is the user is librarian or not

        Returns:
            Bool: if the user is librarian.
        """
        try:
            Librarian.objects.get(user_id=self.id)
            return True
        except Librarian.DoesNotExist:
            return False


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
        return self.name


class Librarian(models.Model):
    """Creates a child table for librarians for managing permission"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class BookLoan(models.Model):
    """This model represents user book loans. Loans are managed by librarians and admins."""

    class BookLoanStatus(models.TextChoices):
        """Enumeration class for book loans statues"""

        REQUESTED = "requested", _("Requested")
        ISSUED = "issued", _("Issued")
        REJECTED = "rejected", _("Rejected")
        RETURNED = "returned", _("Returned")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=BookLoanStatus.choices, default=BookLoanStatus.REQUESTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    date_borrowed = models.DateField(null=True, blank=True)
    date_due = models.DateField(null=True, blank=True)
    date_returned = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.name}"


class BookRequest(models.Model):
    """This model represents unavailable books requested by users"""

    class BookRequestStatus(models.TextChoices):
        """Enumeration class for book request statues"""

        PENDING = "pending", _("Pending")
        APPROVED = "approved", _("Approved")
        REJECTED = "rejected", _("Rejected")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=BookRequestStatus.choices,
        default=BookRequestStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book_name}"
