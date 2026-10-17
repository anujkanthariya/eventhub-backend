from django.urls import path

from .views import (UserRegistrationView, UserProfileView, ChangePasswordView)
from .verification_views import SendEmailVerificationView, ConfirmEmailVerificationView

urlpatterns = [
    path(
        "register/",
        UserRegistrationView.as_view(),
        name="user-register",
    ),
    path(
        "profile/", 
        UserProfileView.as_view(), 
        name="user-profile"),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "email-verification/send/",
        SendEmailVerificationView.as_view(),
        name="email-verification-send",
    ),
    path(
        "email-verification/confirm/",
        ConfirmEmailVerificationView.as_view(),
        name="email-verification-confirm",
    ),
]
