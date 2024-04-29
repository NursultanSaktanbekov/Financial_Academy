from django.core.mail import send_mail

from apps.academy.models import Contact

from config import settings


def send_email(message):
    contact = Contact.objects.first()
    print(contact)
    subject = "Новая форма была заполнена"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [contact.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
