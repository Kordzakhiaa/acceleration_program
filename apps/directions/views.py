from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.directions.models import Direction
from apps.directions.serializers import DirectionsSerializer


@extend_schema(tags=["Directions"])
class DirectionsModelViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DirectionsSerializer
    lookup_field = 'id'
    queryset = Direction.objects.all()
