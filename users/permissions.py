from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in "PATCH":
            return (obj.id== request.user.id)



class MyCustomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if "is_active" in request.data :
                return  request.user.is_superuser