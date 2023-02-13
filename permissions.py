from rest_framework import permissions

class CreateDataPermission(permissions.BasePermission):
    def has_permission(self, request, view): 
        return True

class ReadDataPermission(permissions.BasePermission):
    def has_permission(self, request, view): 
        return True

class UpdateDataPermission(permissions.BasePermission):
    def has_permission(self, request, view): 
        return True

class DeleteDataPermission(permissions.BasePermission):
    def has_permission(self, request, view): 
        return True

class UpdateSpecificFieldsOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): 
        allowed_fields = get_permissions_for_user(request.user, 'update_', 'fields')

        if request.method in permissions.SAFE_METHODS:
            return True
        for field in request.data: 
            if field not in allowed_fields:
                return False
        return True