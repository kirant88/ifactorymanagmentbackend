from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow super admins.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superadmin


class IsLocationAdminOrSuperAdmin(permissions.BasePermission):
    """
    Custom permission to allow location admins and super admins.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_superadmin or request.user.is_location_admin)
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow users to edit their own profile or admins to edit any profile.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow if user is the owner
        if obj == request.user:
            return True
        
        # Allow if user is super admin
        if request.user.is_superadmin:
            return True
        
        # Allow if user is location admin and object is in same location
        if request.user.is_location_admin and obj.location == request.user.location:
            return True
        
        return False


class CanViewLocation(permissions.BasePermission):
    """
    Custom permission to check if user can view data for a specific location.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Super admins can view all locations
        if request.user.is_superadmin:
            return True
        
        # Get location from query params or request data
        location = request.query_params.get('location') or request.data.get('location')
        
        # If no location specified, allow (will be filtered in view)
        if not location:
            return True
        
        # Check if user has access to this location
        return request.user.has_location_access(location)
