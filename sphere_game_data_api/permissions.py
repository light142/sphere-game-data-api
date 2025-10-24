from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Anyone can create (POST) game data
    - Only admin users can read, update, or delete game data
    """

    def has_permission(self, request, view):
        # Allow anyone to create (POST)
        if request.method == 'POST':
            return True
        
        # For all other methods, require admin authentication
        return request.user and request.user.is_authenticated and request.user.is_staff
