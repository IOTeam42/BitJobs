from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        unsafe_methods = ['POST', 'PUT']

        if request.method in unsafe_methods:
            return request.user.is_authenticated()

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.orderer
