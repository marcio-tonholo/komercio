from rest_framework import permissions

class IsProductSeller(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in "GET":
            return True
        if request.method in "PATCH":
            return obj.seller_id.id== request.user.id
        
        


class MyCustomPermission(permissions.BasePermission):

    
    def has_permission(self, request, view):
        if request.method in "GET":
            return True
        
        if request.method in 'POST':
            return (request.user.is_authenticated and request.user.is_seller)

        if request.method in 'PATCH':
            return (request.user.is_authenticated and request.user.is_seller)
        
