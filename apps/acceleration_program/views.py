from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
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


@extend_schema(tags=["Programs"])
class AccelerationProgramViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsStuffAccelerationOrAdminUser)
    queryset = AccelerationProgram.objects.all()
    serializer_class = AccelerationProgramSerializer
    lookup_field = "id"
    http_method_names = ["get", "post", "patch", "delete"]

    def create(self, request: "Request", *args, **kwargs) -> "Response":
        serializer: "AccelerationProgramSerializer" = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer.create_joinprogram_template(instance=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request: "Request", *args, **kwargs) -> "Response":
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.create_joinprogram_template(instance=instance)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # IF 'PREFETCH_RELATED' HAS BEEN APPLIED TO A QUERYSET,
            # WE NEED TO FORCIBLY INVALIDATE THE PREFETCH CACHE ON THE INSTANCE
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Applicants"])
class ApplicantModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisteredApplicantsSerializer
    queryset = Applicants.objects.all()
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicantsRegistrationSerializer
        return self.serializer_class


@extend_schema(tags=["Join Program"])
class JoinProgramListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JoinProgramSerializer
    queryset = JoinProgram.objects.all()
