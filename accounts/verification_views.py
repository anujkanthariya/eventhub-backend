from django.contrib.auth import get_user_model
from django.core import signing

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
        token = request.query_params.get("token")

        if not token:
            return Response(
                {"detail": "Token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            data = signing.loads(
                token,
                salt="accounts.email_verification",
                max_age=60 * 5,
            )
            user = User.objects.get(pk=data["user_id"])
        except (
            signing.BadSignature,
            signing.SignatureExpired,
            User.DoesNotExist,
            KeyError,
            TypeError,
        ):
            return Response(
                {"detail": "Invalid or expired verification token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_email_verified:
            return Response(
                {"detail": "Email is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        return Response(
            {"detail": "Email verified successfully."},
            status=status.HTTP_200_OK,
        )