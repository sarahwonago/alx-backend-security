from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from ipgeolocation import geolocate_ip

from .models import RequestLog, BlockedIP


class IPLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log client IPs, block blacklisted IPs,
    and enrich logs with geolocation data.
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

        # Try to get geolocation from cache
        cache_key = f"geo_{ip}"
        geo_data = cache.get(cache_key)

        if not geo_data and ip:
            try:
                # call API
                geo_data = geolocate_ip(ip)
                cache.set(cache_key, geo_data, 60 * 60 * 24)  # cache for 24 hours
            except Exception:
                geo_data = {"country": None, "city": None}

        # Extract fields safely
        country = geo_data.get("country") if geo_data else None
        city = geo_data.get("city") if geo_data else None

        # Save request log
        try:
            RequestLog.objects.create(
                ip_address=ip, path=request.path, country=country, city=city
            )
        except Exception:
            pass
