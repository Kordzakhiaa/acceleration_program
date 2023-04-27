from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.acceleration_program.views import (
    AccelerationProgramViewSet,
    JoinProgramModelViewSet,
    ApplicantModelViewSet,
    StageModelViewSet,
    ApplicantResponseModelViewSet,
    StuffResponseDescriptionModelViewSet,
)

app_name: str = "acceleration_program"

router = DefaultRouter()
router.register("program", AccelerationProgramViewSet, basename="acceleration_program")
router.register("applicant", ApplicantModelViewSet, basename="applicant")
router.register("stage", StageModelViewSet, basename="stage")
router.register("join_program", JoinProgramModelViewSet, basename="join_program")
router.register("applicant_response", ApplicantResponseModelViewSet, basename="applicant_response")
router.register(
    "stuff_response_with_description", StuffResponseDescriptionModelViewSet, basename="stuff_response_with_description"
)

urlpatterns = [
    path("", include(router.urls)),
]
