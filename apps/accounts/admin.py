from django.contrib import admin

from apps.accounts.models import CustomUserModel

admin.site.register(CustomUserModel)
