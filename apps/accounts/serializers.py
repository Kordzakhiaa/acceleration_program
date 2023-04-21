from typing import OrderedDict

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import CustomUserModel


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True, )
    confirm_password = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = CustomUserModel
        fields = ['email', 'password', 'confirm_password']

    def validate(self, data: "OrderedDict") -> "OrderedDict":
        """This method helps us to validate each step during user registration"""
        if CustomUserModel.objects.filter(email=data.get('email')):
            raise serializers.ValidationError({"email": _("Account with this email already exists.")})
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": _("Passwords Doesn't Match.")})

        del data['confirm_password']  # DELETING EXTRA FIELD TO AVOID UNEXPECTED ARGUMENT

        return data

    def create(self, validated_data: "OrderedDict") -> "CustomUserModel":
        """Overriding this method because we want to use our custom user model create_user method with its logic"""
        instance = CustomUserModel.objects.create_user(**validated_data)
        return instance
