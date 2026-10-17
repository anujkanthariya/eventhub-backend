
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Account APIs: registration, profile, password, email verification
    path("accounts/", include("accounts.urls")),

    # JWT login and refresh
    path(
        "accounts/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "accounts/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
