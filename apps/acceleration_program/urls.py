from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.acceleration_program.views import (
    AccelerationProgramViewSet,
    JoinProgramListAPIView,
    ApplicantModelViewSet,
    StageModelViewSet, OrderedStageModelViewSet
)

app_name: str = "acceleration_program"

router = DefaultRouter()
router.register("program", AccelerationProgramViewSet, basename="acceleration_program")
router.register("applicant", ApplicantModelViewSet, basename="applicant")
router.register("stage", StageModelViewSet, basename="stage")
router.register("ordered_stage", OrderedStageModelViewSet, basename="ordered_stage")

urlpatterns = [
    path("join_program/list/", JoinProgramListAPIView.as_view(), name="join_program_list"),

    path("", include(router.urls)),
]
