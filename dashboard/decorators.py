from django.contrib.auth.decorators import user_passes_test
from rest_framework.permissions import BasePermission

def group_required(*group_names):
   """Requires user membership in at least one of the groups passed in."""

   def in_groups(u):
        if u.is_authenticated:
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
        return False
   return user_passes_test(in_groups)

class ModeratorOnly(BasePermission):
    def has_permission(self, request, view):
      if request.user.groups.filter(name='moderator').exists() or request.user.is_staff or request.user.is_superuser:
         return True
      return False

class MarketingOnly(BasePermission):
    def has_permission(self, request, view):
      if (request.user.groups.filter(name='marketing').exists() and request.user.is_staff) or request.user.is_superuser:
         return True
      return False

class OperatorOnly(BasePermission):
    def has_permission(self, request, view):
      if request.user.groups.filter(name='operator').exists() or request.user.is_staff or request.user.is_superuser:
         return True
      return False

class SuperUserOnly(BasePermission):
    def has_permission(self, request, view):
      if request.user.is_superuser:
         return True
      return False