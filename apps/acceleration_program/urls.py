from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.acceleration_program.views import (
    AccelerationProgramViewSet,
    JoinProgramModelViewSet,
    ApplicantModelViewSet,
    StageModelViewSet
)

app_name: str = "acceleration_program"

router = DefaultRouter()
router.register("program", AccelerationProgramViewSet, basename="acceleration_program")
router.register("applicant", ApplicantModelViewSet, basename="applicant")
router.register("stage", StageModelViewSet, basename="stage")
router.register("join_program", JoinProgramModelViewSet, basename="join_program")

urlpatterns = [

    path("", include(router.urls)),
]
