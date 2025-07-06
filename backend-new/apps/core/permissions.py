"""
Custom permissions for Evolution Digital Market.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for product sellers.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.seller == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsVerifiedUser(permissions.BasePermission):
    """
    Permission for verified users only.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_verified


class CanCreateListing(permissions.BasePermission):
    """
    Permission to check if user can create listings.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return (
                request.user and 
                request.user.is_authenticated and 
                request.user.is_verified and
                not request.user.is_banned
            )
        return True