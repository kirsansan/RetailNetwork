from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "You might see only self-information"

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            # print("qua", request.user.objects.filter(user=request.user))
            # if request.user.objects.filter(user=request.user).exists():
            return True
        return False


class IsAdmin(BasePermission):
    message = "You need to be Admin for this action"

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False
