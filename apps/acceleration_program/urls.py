from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.acceleration_program.views import (
    AccelerationProgramViewSet,
    RegisteredApplicantsListAPIView,
)

app_name: str = "acceleration_program"

router = DefaultRouter()
router.register('acceleration_program', AccelerationProgramViewSet, basename='acceleration_program')

urlpatterns = [
    path('programs/list/', AccelerationProgramViewSet.as_view({'get': 'list'}), name="acceleration_programs"),
    path('program/<int:id>/', AccelerationProgramViewSet.as_view({'get': 'retrieve'}), name="acceleration_program"),
    path('program/create/', AccelerationProgramViewSet.as_view({'post': 'create'}), name="acceleration_programs"),
    path('program/update/<int:id>/', AccelerationProgramViewSet.as_view({'post': 'update'}), name="acceleration_program"),
    path('registered_applicants/', RegisteredApplicantsListAPIView.as_view(), name="registered_applicants"),
]
