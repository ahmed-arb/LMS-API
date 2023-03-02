""" This module has all core app corn jobs"""

from datetime import datetime
import logging

from templated_mail.mail import BaseEmailMessage

from core.models import BookLoan


logger = logging.getLogger(__name__)


def email_overdue_books():
    """cron job for emailing user which have a book overdue"""
    today = datetime.now()
    loan_queryset = BookLoan.objects.select_related('book', 'user').filter(date_due__lt=today)

    for loan in loan_queryset:
        message = BaseEmailMessage(
            template_name="emails/overdue_books.html",
            context={
                "name": loan.user,
                "book": loan.book,
            },
        )
        message.send([loan.user.email])
        logger.info("email sent to %s for %s due: %s", loan.user.email, loan.book, loan.date_due)
