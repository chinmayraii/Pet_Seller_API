from rest_framework import permissions

class IsPetOwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.animal_owner == request.user    