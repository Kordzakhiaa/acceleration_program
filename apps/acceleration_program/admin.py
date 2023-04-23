from django.contrib import admin

from apps.acceleration_program.models import (
    AccelerationProgram,
    Stage,
    JoinProgram,
    Applicants,
    StageType,
    OrderedStages,
    ApplicantResponse,
    StuffResponseDescription
)

admin.site.register(AccelerationProgram)
admin.site.register(Stage)
admin.site.register(JoinProgram)
admin.site.register(Applicants)
admin.site.register(StageType)
admin.site.register(OrderedStages)
admin.site.register(ApplicantResponse)
admin.site.register(StuffResponseDescription)
