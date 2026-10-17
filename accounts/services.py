
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .tokens import email_verification_token


def send_verification_email(user, request):
    # Encode the user's primary key as a URL-safe Base64 string.
    uid = urlsafe_base64_encode(force_bytes(str(user.pk)))

    print("USER PK:", repr(str(user.pk)))
    print("GENERATED UID:", repr(uid))
    print(
        "DECODED UID:",
        repr(urlsafe_base64_decode(uid).decode("ascii")),
    )

    # Generate the verification token.
    token = email_verification_token.make_token(user)

    # Build the confirmation URL.
    verification_path = reverse("email-verification-confirm")
    verification_url = request.build_absolute_uri(
        f"{verification_path}?uid={uid}&token={token}"
    )

    subject = "Verify your EventHub email address"

    message = (
        f"Hello {user.first_name or 'User'},\n\n"
        "Please verify your EventHub email address by opening this link:\n\n"
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
