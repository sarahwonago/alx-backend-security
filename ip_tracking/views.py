from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from ratelimit.decorators import ratelimit
from django.conf import settings


# Anonymous users: 5 requests/minute
@ratelimit(key="ip", rate=settings.RATELIMITS["anonymous"], method="POST", block=True)
# Authenticated users: 10 requests/minute
@ratelimit(
    key="ip", rate=settings.RATELIMITS["authenticated"], method="POST", block=True
)
def login_view(request):
    """
    Example login view protected by IP-based rate limiting.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
