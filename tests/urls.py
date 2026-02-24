from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.staticfiles.views import serve as staticfiles_serve
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from djust_admin import site


@csrf_exempt
def test_login(request):
    """Test-only login endpoint for Playwright tests.

    This bypasses the djust LiveView WebSocket-based login and uses
    traditional Django session authentication.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active and user.is_staff:
            login(request, user)
            next_url = request.GET.get("next", "/admin/")
            return HttpResponseRedirect(next_url)
        return HttpResponse("Login failed", status=401)
    # Render a simple login form
    return HttpResponse(
        """
        <form method="post">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>
        """,
        content_type="text/html",
    )


# Use 2-tuple format: (patterns, app_name)
urlpatterns = [
    path("admin/", include((site.get_urls(), "djust_admin"), namespace=site.name)),
    path("test-login/", test_login, name="test_login"),  # Test-only login
]

# Serve static files during development using staticfiles finders
# This works with Daphne/ASGI (unlike the static() helper which needs STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^static/(?P<path>.*)$",
            staticfiles_serve,
            {"insecure": True},
        ),
    ]
