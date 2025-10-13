from rest_framework.permissions import BasePermission, SAFE_METHODS

# 🔐 Admin-only access
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'

# 🧑 Seller-only access
class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'seller'

# 🛒 Buyer-only access
class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'buyer'

# 🔐 Owner can edit, others read-only
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user or obj.seller == request.user or obj.user == request.user

# 🔐 Authenticated users can read/write, guests read-only
class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated
        )
