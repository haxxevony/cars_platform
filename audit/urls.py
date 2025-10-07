from django.urls import path
from django.http import HttpResponse

def audit_home(request):
    return HttpResponse("📋 Audit module is wired.")

urlpatterns = [
    path('', audit_home, name='audit-home'),
]
