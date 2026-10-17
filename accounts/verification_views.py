import uuid

from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import send_verification_email
from .tokens import email_verification_token

User = get_user_model()

class SendEmailVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.is_email_verified:
            return Response(
                {"detail": "Email is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        send_verification_email(user, request)

        return Response(
            {"detail": "Verification email sent."},
            status=status.HTTP_200_OK,
        )



class ConfirmEmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        uidb64 = request.query_params.get("uid")
        token = request.query_params.get("token")

        if not uidb64 or not token:
            return Response(
                {"detail": "User identifier and token are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Decode the URL-safe Base64 UID.
            decoded_uid = force_str(urlsafe_base64_decode(uidb64))
            user_uuid = uuid.UUID(decoded_uid)

            # Find the user using the UUID primary key.
            user = User.objects.get(pk=user_uuid)

        except (
            ValueError,
            TypeError,
            UnicodeDecodeError,
            User.DoesNotExist,
        ):
            return Response(
                {"detail": "Invalid user identifier in verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_email_verified:
            return Response(
                {"detail": "Email is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not email_verification_token.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired verification token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        return Response(
            {"detail": "Email verified successfully."},
            status=status.HTTP_200_OK,
        )

