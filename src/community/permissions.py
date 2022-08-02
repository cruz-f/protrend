class CommunityPermissionsMixIn:

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated and request.user.is_active:
            return True

        return False

    def has_add_permission(self, request, obj=None):
        if request.user.is_authenticated and request.user.is_active:
            return True

        return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return self.has_view_permission(request)

        else:
            if request.user.is_superuser:
                return True

            elif request.user == obj.user and request.user.is_active:
                return True

            else:
                return False

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return self.has_view_permission(request)

        else:
            if request.user.is_superuser:
                return True

            elif request.user == obj.user and request.user.is_active:
                return True

            else:
                return False
