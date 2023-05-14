from django.contrib import admin

from apps.acceleration_program.models import (
    AccelerationProgram,
    Stage,
    JoinProgram,
    Applicants,
    AssignmentType,
    Assignment,
    ApplicantResponse,
    StuffFinalResponseDescription,
    StuffMembersResponse
)

admin.site.register(AccelerationProgram)
admin.site.register(Stage)
admin.site.register(JoinProgram)
admin.site.register(Applicants)
admin.site.register(AssignmentType)
admin.site.register(Assignment)
admin.site.register(ApplicantResponse)
admin.site.register(StuffFinalResponseDescription)
admin.site.register(StuffMembersResponse)
