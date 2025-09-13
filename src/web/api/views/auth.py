from django.shortcuts import redirect
from django.views.generic import TemplateView


class WebLoginView(TemplateView):
    """Web login view with security headers"""
    template_name = "web/login.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        # Avoid caching
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        # Allow popup
        response["Cross-Origin-Opener-Policy"] = "unsafe-none"
        response["Cross-Origin-Embedder-Policy"] = "unsafe-none"

        # CSP: allow Google Identity Services and external resources; keep everything else local/simple
        response["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://accounts.google.com https://*.gstatic.com https://cdn.skypack.dev; "
            "style-src 'self' 'unsafe-inline' https://unpkg.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https://*.gstatic.com; "
            "connect-src 'self' https://accounts.google.com https://*.gstatic.com; "
            "frame-src https://accounts.google.com;"
        )
        return response


class WebRegisterView(TemplateView):
    """Web register view with security headers"""
    template_name = "web/register.html"
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        # Avoid caching
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        # Allow popup
        response["Cross-Origin-Opener-Policy"] = "unsafe-none"
        response["Cross-Origin-Embedder-Policy"] = "unsafe-none"

        # CSP: allow Google Identity Services and external resources; keep everything else local/simple
        response["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://accounts.google.com https://*.gstatic.com https://cdn.skypack.dev; "
            "style-src 'self' 'unsafe-inline' https://unpkg.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https://*.gstatic.com; "
            "connect-src 'self' https://accounts.google.com https://*.gstatic.com; "
            "frame-src https://accounts.google.com;"
        )
        return response


class WebChangePasswordView(TemplateView):
    """Web change password view"""
    template_name = "web/change-password.html"


def web_logout_view(request):
    """Web logout view that clears cookies and redirects to login"""
    response = redirect('web:login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response 