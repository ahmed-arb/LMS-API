from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import F

from templated_mail.mail import BaseEmailMessage

from .models import Book, BookLoan, BookRequest


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


@receiver(pre_save, sender=BookRequest)
def notify_user(sender, **kwargs):
    request_instance: BookRequest = kwargs["instance"]
    if request_instance.id is None:  # new object will be created
        pass
    else:
        loan_previous = BookRequest.objects.get(id=request_instance.id)
        if loan_previous.status != request_instance.status:  # status updated
            if request_instance.status == "rejected":
                message = BaseEmailMessage(
                    template_name="emails/book_request_rejected.html",
                    context={
                        "name": request_instance.user,
                        "book": request_instance.book_name,
                        "reason": request_instance.reason,
                    },
                )
                message.send([request_instance.user.email])
