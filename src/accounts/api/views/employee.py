from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from accounts.models import Employee
from accounts.permissions import RoleBasedPermission
from ..serializers.employee import EmployeeSerializer

class EmployeeCreateView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                employee = serializer.save()
                return Response({
                    "success": True,
                    "message": "Employee created successfully!",
                    "employee": EmployeeSerializer(employee, context={'request': request}).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                if hasattr(e, 'detail'):
                    return Response({
                        "success": False,
                        "message": "Validation failed",
                        "errors": e.detail
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        "success": False,
                        "message": "Failed to create employee. Please try again."
                    }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "success": False,
                "message": "Invalid data provided",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get(self, request):
        try:
            search = request.GET.get('search', '').strip()
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            
            employees = Employee.objects.all()
            
            if search:
                employees = employees.filter(
                    Q(name__icontains=search) |
                    Q(designation__icontains=search) |
                    Q(department__icontains=search) |
                    Q(employee_id__icontains=search) |
                    Q(user__email__icontains=search)
                )
            
            employees = employees.order_by('-created_at')
            
            total_count = employees.count()
            total_pages = (total_count + page_size - 1) // page_size
            
            start = (page - 1) * page_size
            end = start + page_size
            employees = employees[start:end]
            
            serializer = EmployeeSerializer(employees, many=True, context={'request': request})
            
            return Response({
                "success": True,
                "employees": serializer.data,
                "pagination": {
                    "current_page": page,
                    "total_pages": total_pages,
                    "total_count": total_count,
                    "page_size": page_size,
                    "has_next": page < total_pages,
                    "has_previous": page > 1
                }
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to fetch employees: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get(self, request, employee_id):
        try:
            employee = get_object_or_404(Employee, employee_id=employee_id)
            serializer = EmployeeSerializer(employee, context={'request': request})
            return Response({
                "success": True,
                "employee": serializer.data
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to fetch employee: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmployeeUpdateView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def put(self, request, employee_id):
        try:
            employee = get_object_or_404(Employee, employee_id=employee_id)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Employee updated successfully!",
                    "employee": EmployeeSerializer(employee, context={'request': request}).data
                })
            else:
                return Response({
                    "success": False,
                    "message": "Invalid data provided",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to update employee: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmployeeDeleteView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    
    def delete(self, request, employee_id):
        try:
            employee = get_object_or_404(Employee, employee_id=employee_id)
            employee_name = employee.name
            employee.delete()
            return Response({
                "success": True,
                "message": f"Employee '{employee_name}' deleted successfully!"
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to delete employee: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 