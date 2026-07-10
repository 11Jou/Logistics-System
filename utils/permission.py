from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'

class IsDispatcher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'dispatcher'

class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'driver'

class IsManagerOrDispatcher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'manager' or request.user.role == 'dispatcher')