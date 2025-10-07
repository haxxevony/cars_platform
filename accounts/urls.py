from django.urls import path
from django.http import HttpResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import register_view, home_view

# 🏠 Health Check View
def account_home(request):
    return HttpResponse("✅ Accounts module is wired.")

# 🔐 Auth Endpoints + Health Check + Registration
urlpatterns = [
    path('', account_home, name='account-home'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
]
