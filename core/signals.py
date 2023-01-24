from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import F

from .models import Book, BookLoan


@receiver(pre_save, sender=BookLoan)
def update_inventory(sender, **kwargs):
    loan_instance: BookLoan = kwargs["instance"]
    if loan_instance.id is None:  # new object will be created
        pass
    else:
        loan_previous = BookLoan.objects.get(id=loan_instance.id)
        if loan_previous.status != loan_instance.status:  # status updated
            if loan_instance.status == "issued":
                Book.objects.filter(pk=loan_instance.book.id).update(stock=F("stock") - 1)
            elif loan_instance.status == "returned":
                Book.objects.filter(pk=loan_instance.book.id).update(stock=F("stock") + 1)
