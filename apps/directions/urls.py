from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.directions.views import DirectionsModelViewSet

app_name: str = "acceleration_program"

router = DefaultRouter()
router.register('direction', DirectionsModelViewSet, basename='direction')

urlpatterns = [
    path('', DirectionsModelViewSet.as_view({'get': 'list'}), name="directions"),
    path('<int:id>/', DirectionsModelViewSet.as_view({'get': 'retrieve'}), name="direction"),
]
