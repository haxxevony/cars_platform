from .models import AuditLog

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            AuditLog.objects.create(
                user=request.user,
                path=request.path,
                method=request.method,
                status_code=response.status_code
            )
        return response
