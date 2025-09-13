from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import AppSettings
from accounts.models import Student
from .serializers import AppSettingsSerializer
import string

class AppSettingsView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = AppSettingsSerializer

    def get_object(self):
        # First ensure the settings exist
        settings = AppSettings.get_solo()
        # Then get it with prefetch_related to avoid N+1 queries
        return AppSettings.objects.prefetch_related('media').get(pk=settings.pk)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, context={'request': request})
        
        # Additional stats
        total_students = Student.objects.count()
        total_courses = Course.objects.count()
        students_with_jobs = Job.objects.filter(student__isnull=False).values('student').distinct().count()
        percentage_with_jobs = (
            (students_with_jobs / total_students) * 100 if total_students > 0 else 0
        )

        # Prepare sanitized response
        response_data = {
            "success": True,
            "message": "About page data retrieved successfully!",
            "details": {
                "name": serializer.data.get("name"),
                "logo": serializer.data.get("logo"),
                "description": serializer.data.get("description"),
            },
            "media": serializer.data.get("media", []),
            "stats": [
                {
                    "displayname": "Total Student Count",
                    "icon": "switch.png",
                    "value": str(total_students)
                },
                {
                    "displayname": "Total Courses Offered",
                    "icon": "approveleave.png",
                    "value": str(total_courses)
                },
                {
                    "displayname": "Total Offered Jobs",
                    "icon": "studentdetails.png",
                    "value": str(students_with_jobs)
                },
                {
                    "displayname": "% Students with Jobs",
                    "icon": "salaryslip.png",
                    "value": str(round(percentage_with_jobs, 2))
                }
            ]
        }

        response = Response(response_data)

        # Add ETag and Last-Modified headers
        response['ETag'] = f'"{obj.updated_at.isoformat()}"'
        response['Last-Modified'] = obj.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        return response

    def post(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Method not allowed'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def put(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Method not allowed'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def patch(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Method not allowed'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def delete(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Method not allowed'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        ) 

class GetlogoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        app_version = request.data.get("appversion")
        platform = request.data.get("platform")

        # Get first record from AppSettings
        app_setting = AppSettings.objects.first()
        if not app_setting:
            return Response({
                "success": False,
                "message": "App settings not found."
            }, status=status.HTTP_404_NOT_FOUND)

        # Update fields if provided
        if app_version:
            app_setting.appversion = app_version
        if platform:
            app_setting.platform = platform
        app_setting.save(update_fields=["appversion", "platform"])

        # Validate version rules
        invalid_version = False
        if platform and app_version:
            if platform.lower() == "android" and app_version not in ["1.0.0", "1.2","2.0"]:
                invalid_version = True
            elif platform.lower() == "ios" and app_version not in ["2.0", "2.3"]:
                invalid_version = True

        if invalid_version:
            return Response({
                "success": False,
                "errormsg": "Kindly update app from Play Store or App Store",
                "newandroidlink": "https://play.google.com/store/apps/details?id=com.radicallogix.studentsapp&hl=en_IN",
                "newioslink": "https://apps.apple.com/in/app/radical-logix/id1583937597"
            }, status=status.HTTP_426_UPGRADE_REQUIRED)  # 426 = Upgrade Required

        # Return logo if everything is fine
        if not app_setting.logo:
            return Response({
                "success": False,
                "message": "Logo not found."
            }, status=status.HTTP_404_NOT_FOUND)

        logo_url = request.build_absolute_uri(app_setting.logo.url)

        return Response({
            "success": True,
            "logo_url": logo_url  # assuming logo field stores the full URL
        }, status=status.HTTP_200_OK)