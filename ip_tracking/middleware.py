from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog, BlockedIP


class IPLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log client IPs and block requests from blacklisted IPs.
    """

    def process_request(self, request):
        # Extract client IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        # Block if IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Forbidden: Your IP is blocked.")

        # Otherwise, log request
        try:
            RequestLog.objects.create(ip_address=ip, path=request.path)
        except Exception:
            # Fail silently to avoid breaking requests
            pass
