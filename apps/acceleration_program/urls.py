from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.acceleration_program.views import (
    AccelerationProgramViewSet,
)

app_name: str = "acceleration_program"

router = DefaultRouter()
router.register('acceleration_program', AccelerationProgramViewSet, basename='acceleration_program')

urlpatterns = [
    path('list/', AccelerationProgramViewSet.as_view({'get': 'list'}), name="acceleration_programs"),
    path('<int:id>/', AccelerationProgramViewSet.as_view({'get': 'retrieve'}), name="acceleration_program"),
    path('create/', AccelerationProgramViewSet.as_view({'post': 'create'}), name="acceleration_programs"),
    path('update/<int:id>/', AccelerationProgramViewSet.as_view({'post': 'update'}), name="acceleration_program"),
]
