from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import models
from accounts.permissions import RoleBasedPermission
from django.db.models import Count, Q
from datetime import date
from accounts.models import Student, Employee, User
from app_settings.models import AppSettings
from accounts.api.serializers.employee import EmployeeSerializer
from app_settings.serializers import AppSettingsSerializer
from django.shortcuts import get_object_or_404

class WebDashboardView(TemplateView):
    """Web dashboard view with cache control"""
    template_name = "web/dashboard.html"
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # Add cache control headers to prevent back button issues
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response