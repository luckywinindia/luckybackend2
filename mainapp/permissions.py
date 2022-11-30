from rest_framework.permissions import BasePermission
from .models import Profile



SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    message = "You are not logged in !"
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated):
            return True
        return False

class IsBrokerOrReadOnly(BasePermission):
    message = "You are not registered as a broker !"
    def has_permission(self, request, view):
        if (request.user.profile.profile_type == 3):
            return True
        return False

class IsAdminOrReadOnly(BasePermission):
    message = "You are not registered as an admin !"
    def has_permission(self, request, view):
        if (request.user.profile.profile_type == 1):
            return True
        return False

class IsManagerOrReadOnly(BasePermission):
    message = "You are not registered as a manager !"
    def has_permission(self, request, view):
        if (request.user.profile.profile_type == 2):
            return True
        return False
        