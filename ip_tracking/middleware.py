from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog


class IPLoggingMiddleware(MiddlewareMixin):
    """
    Log client IP, path and timestamp for every request.
    Uses REMOTE_ADDR or X-Forwarded-For if present.
    """

    def process_request(self, request):
        # get client IP (basic)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # X-Forwarded-For may be a comma-separated list; take first
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        # Save a log entry; keep this inside try/except to avoid breaking the request flow
        try:
            RequestLog.objects.create(ip_address=ip, path=request.path)
        except Exception:
            pass
