import os
from celery import Celery
from django.utils import timezone
from django.core.mail import send_mail
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

app = Celery('library_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(
        crontab(hour=5, minute=3),
        check_overdue_loans.s(),
    )

def check_overdue_loans():
    print("Running")
    from library.models import Loan

    now = timezone.now()
    overdue_loans = Loan.objects.filter(is_returned=False, due_date__lte=now)

    for loan in overdue_loans:
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Return Overdue',
            message=f'Hello {loan.member.user.username},\n\nYou have not returned your overdue book: "{book_title}".\nPlease return it as soon as possible.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
