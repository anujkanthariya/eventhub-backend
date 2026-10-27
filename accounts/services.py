from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.core import signing

from .tokens import email_verification_token


def send_verification_email(user, request):
    token = signing.dumps(
        {"user_id": str(user.pk)},
        salt="accounts.email_verification",
    )

    verification_path = reverse("email-verification-confirm")
    query_string = urlencode({"token": token})

    verification_url = request.build_absolute_uri(
        f"{verification_path}?{query_string}"
    )

    subject = "Verify your EventHub email address"
    message = (
        f"Hello {user.first_name or 'User'},\n\n"
        "Please verify your EventHub email address by opening "
        "this link:\n\n"
        f"{verification_url}\n\n"
        "If you did not request this email, you can ignore it."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )