from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStuffAccelerationOrAdminUser(BasePermission):
    """Allows access only to the acceleration stuff members or users with the admin statuses."""

    message = "You do not have permission to perform this action because you are not acceleration program stuff"

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS or request.user.user_type in ["Stuff-Acceleration", "Admin"]
