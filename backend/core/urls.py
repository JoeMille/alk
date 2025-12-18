from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # Added /
    path(
        "api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Added /
    path("api/", include("chat.urls")),
    path("api/users/", include("users.urls")),
]
