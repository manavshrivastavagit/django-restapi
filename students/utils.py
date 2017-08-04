import uuid

from django.conf import settings
from django.core.mail import send_mail


def generate_activation_key():
    return uuid.uuid4().hex


def send_verification_email(user):
    client_url = 'http://elsyser.aerobatic.io/auth/activate/{activation_key}/'.format(
        activation_key=user.student.activation_key
    )

    subject = 'ELSYSER Account activation'
    message = '''Hello, {full_name}!
Visit this link to activate your ELSYSER account: {url}
    '''.format(full_name=user.get_full_name(), url=client_url)

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )