from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.acceleration_program.views import (
    AccelerationProgramViewSet,
    RegisteredApplicantsListAPIView,
    JoinProgramListAPIView,
    RegisterApplicantCreateAPIView,
)

app_name: str = "acceleration_program"

router = DefaultRouter()
router.register("program", AccelerationProgramViewSet, basename="acceleration_program")

urlpatterns = [
    path("registered_applicants/", RegisteredApplicantsListAPIView.as_view(), name="registered_applicants"),
    path("join_program/list/", JoinProgramListAPIView.as_view(), name="join_program_list"),
    path("applicant/register/", RegisterApplicantCreateAPIView.as_view(), name="register_applicant"),

    path("", include(router.urls)),
]
