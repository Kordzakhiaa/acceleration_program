from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.acceleration_program.models import AccelerationProgram
from apps.acceleration_program.serializers import AccelerationProgramSerializer
from apps.accounts.permissions import IsStuffAccelerationOrAdminUser


class AccelerationProgramViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsStuffAccelerationOrAdminUser)
    serializer_class = AccelerationProgramSerializer
    lookup_field = 'id'
    queryset = AccelerationProgram.objects.all()
