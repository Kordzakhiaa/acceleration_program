from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.acceleration_program.models import (
    AccelerationProgram,
    Applicants,
    JoinProgram,
)
from apps.acceleration_program.serializers import (
    AccelerationProgramSerializer,
    RegisteredApplicantsSerializer,
    JoinProgramSerializer,
    ApplicantsRegistrationSerializer,
)
from apps.accounts.permissions import IsStuffAccelerationOrAdminUser


class AccelerationProgramViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsStuffAccelerationOrAdminUser)
    serializer_class = AccelerationProgramSerializer
    lookup_field = "id"
    queryset = AccelerationProgram.objects.all()

    def create(self, request: "Request", *args, **kwargs) -> "Response":
        serializer: "AccelerationProgramSerializer" = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer.create_joinprogram_template(instance=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisteredApplicantsListAPIView(ListAPIView):
    serializer_class = RegisteredApplicantsSerializer
    queryset = Applicants.objects.all()


class JoinProgramListAPIView(ListAPIView):
    serializer_class = JoinProgramSerializer
    queryset = JoinProgram.objects.all()


# TODO: pending applicants are saved we need to dont! only accepted


class RegisterApplicant(CreateAPIView):
    serializer_class = ApplicantsRegistrationSerializer
    queryset = Applicants.objects.all()

    def create(self, request: "Request", *args, **kwargs) -> "Response":
        serializer = self.get_serializer(data=request.data, context={"applicant": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
