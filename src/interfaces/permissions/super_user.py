from rest_framework import permissions


class SuperUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to edit records in the protrend database.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # otherwise, only superusers should be able to edit the protrend database using the api
        if request.user.is_superuser or request.user.is_staff:
            return True

        return False
