from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.acceleration_program.models import AccelerationProgram, Applicants
from apps.acceleration_program.serializers import (
    AccelerationProgramSerializer,
    RegisteredApplicantsSerializer
)
from apps.accounts.permissions import IsStuffAccelerationOrAdminUser


class AccelerationProgramViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsStuffAccelerationOrAdminUser)
    serializer_class = AccelerationProgramSerializer
    lookup_field = 'id'
    queryset = AccelerationProgram.objects.all()


class RegisteredApplicantsListAPIView(ListAPIView):
    serializer_class = RegisteredApplicantsSerializer
    queryset = Applicants.objects.all()
