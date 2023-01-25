from templated_mail.mail import BaseEmailMessage

from datetime import datetime

from core.models import BookLoan


def email_overdue_books():
    today = datetime.now()
    loan_queryset = BookLoan.objects.select_related("book").select_related('user').filter(date_due__lt=today)

    for loan in loan_queryset:
        try:
            # send_mail(subject, message, from_email, recipient_list.append(loan.user.email))
            message = BaseEmailMessage(
                template_name="emails/overdue_books.html",
                context={
                    "name": loan.user,
                    "book": loan.book,
                },
            )
            message.send([loan.user.email])
            print(today, loan.user.email, loan.book, loan.date_due)

        except:
            print("failed")
