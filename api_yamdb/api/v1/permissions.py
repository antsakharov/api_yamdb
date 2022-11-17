from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin)


class ReadOnlyOrIsAdminOrModeratorOrAuthor(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            request.user.is_moderator
            or request.user.is_admin
            or request.user == obj.author)


class ListOrAdminModeratorOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_authenticated
            and request.user.is_admin
        )