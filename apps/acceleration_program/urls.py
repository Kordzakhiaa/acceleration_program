from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.acceleration_program.views import (
    AccelerationProgramViewSet,
    JoinProgramModelViewSet,
    ApplicantModelViewSet,
    StageModelViewSet,
    ApplicantResponseModelViewSet,
    StuffFinalResponseDescriptionModelViewSet,
    StuffMembersResponseModelViewSet,
)

app_name: str = "acceleration_program"

router = DefaultRouter()
router.register("program", AccelerationProgramViewSet, basename="acceleration_program")
router.register("applicant", ApplicantModelViewSet, basename="applicant")
router.register("stage", StageModelViewSet, basename="stage")
router.register("join_program", JoinProgramModelViewSet, basename="join_program")
router.register("applicant_response", ApplicantResponseModelViewSet, basename="applicant_response")
router.register(
    "stuff_final_response_with_description",
    StuffFinalResponseDescriptionModelViewSet,
    basename="stuff_final_response_with_description",
)
router.register(
    "stuff_member_response",
    StuffMembersResponseModelViewSet,
    basename="stuff_member_response",
)

urlpatterns = [
    path("", include(router.urls)),
]
