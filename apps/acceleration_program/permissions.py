from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStuffAccelerationOrAdminUser(BasePermission):
    """Allows access only to the acceleration stuff members or users with the admin statuses."""

    message = "You do not have permission to perform this action because you are not acceleration program stuff"

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS or request.user.user_type in ["Stuff-Acceleration", "Admin"]


class IsOwnerAdminStuffOrReadOnly(BasePermission):
    """
    Object-level permission to only allow updating for owner users or privileged users
    """

    def has_object_permission(self, request, view, obj) -> bool:
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        return obj.applicant == request.user or request.user.user_type in ["Stuff-Acceleration", "Admin"]
