from django.urls import path

from apps.accounts.views import (
    RegistrationAPIView,
    LoginAPIView,
)

app_name: str = "accounts"

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
