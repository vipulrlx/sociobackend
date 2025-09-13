from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import models
from django.db.models import Count, Q
from accounts.permissions import RoleBasedPermission
from django.shortcuts import get_object_or_404
from accounts.models import Menu

class Webview1View(APIView):
    """Web view 1 to return 1"""
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get(self, request):

        try:
            webviewname = 'getwebview1'

            menu = get_object_or_404(Menu, name__icontains=webviewname, is_active=True)

            return Response({
                    "success": True,
                    "message": "URL fetched successfully!",
                    "data":menu.destination_url
                }, status=200)
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to retrieve URL: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        