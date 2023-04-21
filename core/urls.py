from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # PROJECT APPS ENDPOINTS
    path('api/auth/', include('apps.accounts.urls')),

    # THIRD-PARTY APPS ENDPOINTS
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
