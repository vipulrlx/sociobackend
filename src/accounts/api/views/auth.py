from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from accounts.models import User, Employee, Student, Onetimepassword, Role
from ..serializers.auth import RegisterSerializer
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
import json, random, string, hashlib

def detect_platform(request):
    """
    Detect if request is coming from web or mobile based on User-Agent header.
    
    This function checks the User-Agent string for common mobile device indicators
    like 'android', 'iphone', 'ipad', etc. If any mobile indicator is found,
    it returns 'mobile', otherwise it defaults to 'web'.
    
    Args:
        request: Django request object
        
    Returns:
        str: 'web' or 'mobile' based on User-Agent detection
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    
    # Check for mobile indicators
    mobile_indicators = [
        'android', 'iphone', 'ipad', 'ipod', 'blackberry', 
        'windows phone', 'mobile', 'tablet'
    ]
    
    for indicator in mobile_indicators:
        if indicator in user_agent:
            return 'mobile'
    
    # Default to web if no mobile indicators found
    return 'web'

def get_user_phone(user):
    """
    Get phone number from user's associated profile (Student or Employee)
    
    Args:
        user: User instance
        
    Returns:
        str: Phone number or empty string if not found
    """
    try:
        # Check if user has a student profile
        student = user.students.first()
        if student and student.contact_number:
            return student.contact_number
        
        # Check if user has an employee profile
        employee = user.employees.first()
        if employee and employee.contact_number:
            return employee.contact_number
        
        return ""
    except Exception:
        return ""

def get_user_name(user):
    """
    Get name from user's associated profile (Student or Employee)
    
    Args:
        user: User instance
        
    Returns:
        str: Name or empty string if not found
    """
    try:
        # Check if user has a student profile
        student = user.students.first()
        if student and student.full_name:
            return student.full_name
        
        # Check if user has an employee profile
        employee = user.employees.first()
        if employee and employee.name:
            return employee.name
        
        return ""
    except Exception:
        return ""

def get_user_photo_url(user, request):
    """
    Get photo URL from user's associated profile (Student or Employee)
    
    Args:
        user: User instance
        request: Request instance for building absolute URLs
        
    Returns:
        str: Photo URL or None if not found
    """
    try:
        # Check if user has a student profile
        student = user.students.first()
        if student and hasattr(student, 'photo') and student.photo:
            return request.build_absolute_uri(student.photo.url)
        
        # Check if user has an employee profile
        employee = user.employees.first()
        if employee and employee.photo:
            return request.build_absolute_uri(employee.photo.url)
        
        return None
    except Exception:
        return None

def get_user_country_code(user):
    """
    Get country code from user's associated profile (Student or Employee)
    
    Args:
        user: User instance
        
    Returns:
        str: Country code or "+91" as default if not found
    """
    try:
        # Check if user has a student profile
        student = user.students.first()
        if student and student.country_code:
            return student.country_code
        
        # Check if user has an employee profile
        employee = user.employees.first()
        if employee and employee.country_code:
            return employee.country_code
        
        return "+91"  # Default country code
    except Exception:
        return "+91"

def create_user_profile(user, platform, name=None, category=None, phone="", country_code="+91"):
    """
    Create Employee or Student entry based on category parameter or platform.
    
    This function creates the appropriate profile entry based on the following logic:
    - If category parameter is available and equals 'student': Creates a Student entry
    - If category parameter is available and equals anything else: Creates an Employee entry
    - If category parameter is not available: Uses platform-based logic
        - For 'web' platform: Creates an Employee entry
        - For 'mobile' platform: Creates a Student entry
    
    Args:
        user: User instance to associate with the profile
        platform: 'web' or 'mobile' platform identifier
        name: Optional name for the profile (defaults to email prefix)
        category: Optional category parameter ('student' or any other value)
        phone: Phone number (defaults to empty string)
        country_code: Country code for phone numbers (defaults to "+91")
    """
    if not name:
        name = user.email.split('@')[0]
    
    if category is not None:
        if category.lower() == 'student':
            Student.objects.create(
                user=user,
                full_name=name,
                enrollment_date=timezone.now().date(),
                contact_number=phone,
                country_code=country_code,
            )

            # Auto-assign Student role if available
            try:
                student_role = Role.objects.get(name='Student', is_active=True)
                user.role = student_role
                user.save(update_fields=['role'])
                print(f"✅ Auto-assigned Student role to user {user.email}")
            except Role.DoesNotExist:
                # Student role doesn't exist, user will have no role
                print(f"⚠️  Student role not found for user {user.email}")
                pass
        else:
            Employee.objects.create(
                user=user,
                name=name,
                designation="Employee",  # Default designation
                department="General",    # Default department
                joining_date=timezone.now().date(),
                contact_number=phone,
                country_code=country_code,
            )
    else:
        # Use platform-based logic when category is not provided
        if platform == 'web':
            Employee.objects.create(
                user=user,
                name=name,
                designation="Employee",  # Default designation
                department="General",    # Default department
                joining_date=timezone.now().date(),
                contact_number=phone,
                country_code=country_code,
            )
        else:
            Student.objects.create(
                user=user,
                full_name=name,
                enrollment_date=timezone.now().date(),
                contact_number=phone,
                country_code=country_code,
            )

            # Auto-assign Student role if available
            try:
                student_role = Role.objects.get(name='Student', is_active=True)
                user.role = student_role
                user.save(update_fields=['role'])
                print(f"✅ Auto-assigned Student role to user {user.email}")
            except Role.DoesNotExist:
                # Student role doesn't exist, user will have no role
                print(f"⚠️  Student role not found for user {user.email}")
                pass

class CategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        cat_data = ['Student','Employee']
        response = Response({
            "success": True,
            "categorylist": cat_data
        }, status=201)
        
        return response
        

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Get platform from request parameter, default to 'web' if not provided
            platform = request.data.get('platform', 'web')
            
            # automatic platform detection for future use
            # platform = detect_platform(request)

            data = request.data.copy()
            data['platform'] = platform
            
            serializer = RegisterSerializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            response = Response({
                "success": True,
                "message": "User registered successfully!",
                "user": serializer.data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=201)
            
            # Set cookies for backend authentication (30 days = 30 * 24 * 60 * 60 seconds)
            response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=False, samesite='Lax', max_age=2592000)
            response.set_cookie('refresh_token', str(refresh), httponly=True, secure=False, samesite='Lax', max_age=2592000)
            
            return response
        except serializers.ValidationError as e:
            first_error = None
            if hasattr(e, 'detail') and isinstance(e.detail, dict):
                # Get the first error message from the first field
                for field, errors in e.detail.items():
                    if errors:
                        if isinstance(errors, list):
                            first_error = errors[0]
                        else:
                            first_error = str(errors)
                        break
            
            # If no specific error found, use a generic message
            if not first_error:
                first_error = "Registration failed. Please check your data and try again."
            
            return Response({
                "success": False,
                "message": first_error,
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Registration failed. Please check your data and try again.",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        device_token_key = request.data.get("device_token_key")
        
        if not email or not password:
            return Response({
                "success": False,
                "message": "Email and password are required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "message": "No active account found for this email."
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.status != User.Status.ACTIVE:
            return Response({
                "success": False,
                "message": "Account is not active."
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(email=email, password=password)
        if not user:
            return Response({
                "success": False,
                "message": "Password incorrect."
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if device_token_key:
            user.device_token_key = device_token_key
            user.save(update_fields=['device_token_key'])
        

        # Determine user type
        user_type = "other"
        if hasattr(user, 'employees') and user.employees.exists():
            user_type = "employee"
        elif hasattr(user, 'students') and user.students.exists():
            user_type = "student"
            
        refresh = RefreshToken.for_user(user)
        response = Response({
            "success": True,
            "message": "Login successful!",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "email": user.email,
                "contact_number": get_user_phone(user),
                "country_code": get_user_country_code(user),
                "name": get_user_name(user),
                "photo_url": get_user_photo_url(user, request),
                "status": user.status,
                "device_token_key": user.device_token_key,
                "user_type": user_type,
            }
        })
        
        # Set cookies for backend authentication (30 days = 30 * 24 * 60 * 60 seconds)
        response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=False, samesite='Lax', max_age=2592000)
        response.set_cookie('refresh_token', str(refresh), httponly=True, secure=False, samesite='Lax', max_age=2592000)
        
        return response

class LoginotpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        otp = request.data.get("otp")
        
        if not username or not otp:
            return Response({
                "success": False,
                "message": "Username and otp are required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate cutoff time (10 minutes ago)
        cutoff_time = timezone.now() - timedelta(minutes=10)

        # Check if OTP is valid and recent
        otp_entry = Onetimepassword.objects.filter(
            user_id=username,
            otp=otp,
            created_at__gte=cutoff_time
        ).order_by('-created_at').first()

        if otp_entry:

            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "No active account found for this email."
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            if user.status != User.Status.ACTIVE:
                return Response({
                    "success": False,
                    "message": "Account is not active."
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Determine user type
            user_type = "other"
            if hasattr(user, 'employees') and user.employees.exists():
                user_type = "employee"
            elif hasattr(user, 'students') and user.students.exists():
                user_type = "student"
                
            refresh = RefreshToken.for_user(user)
            response = Response({
                "success": True,
                "message": "Login successful!",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "email": user.email,
                    "contact_number": get_user_phone(user),
                    "country_code": get_user_country_code(user),
                    "name": get_user_name(user),
                    "photo_url": get_user_photo_url(user, request),
                    "status": user.status,
                    "device_token_key": user.device_token_key,
                    "user_type": user_type,
                }
            })
            
            # Set cookies for backend authentication (30 days = 30 * 24 * 60 * 60 seconds)
            response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=False, samesite='Lax', max_age=2592000)
            response.set_cookie('refresh_token', str(refresh), httponly=True, secure=False, samesite='Lax', max_age=2592000)
            
            return response

        else:
            return Response({
                "success": False,
                "message": "Invalid or expired OTP."
            }, status=status.HTTP_400_BAD_REQUEST)

class ResendotpView(APIView):
    permission_classes = [AllowAny]

    def generate_otp(self, length=4):
        """Generate a random numeric OTP"""
        return ''.join(random.choices(string.digits, k=length))

    def post(self, request):
        contactnumber = request.data.get("contactnumber")
        
        if not contactnumber:
            return Response({
                "success": False,
                "message": "Mobile Number is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check Student
        student = Student.objects.filter(contact_number=contactnumber).select_related('user').first()
        
        # Check Employee if not found in Student
        employee = None
        if not student:
            employee = Employee.objects.filter(contact_number=contactnumber).select_related('user').first()

        if employee or student:
            # Generate OTP
            otp = self.generate_otp()
            otp = '1234'

            # Determine user object and contact
            if employee:
                user_email = str(employee.user.email)
                contact_number = employee.contact_number
                user_type = "employee"
            else:
                user_email = str(student.user.email)
                contact_number = student.contact_number
                user_type = "student"

            # Get last sequence_no for this user
            last_otp = Onetimepassword.objects.filter(user_id=user_email).order_by('-created_at').first()
            sequence_no = (last_otp.sequence_no + 1) if last_otp else 1

            # Save OTP in database
            Onetimepassword.objects.create(
                user_id=user_email,
                service="Login via OTP",
                otp=otp,
                sent_time=timezone.now(),
                via_sms="1",
                sequence_no=sequence_no
            )

            return Response({
                "success": True,
                "message": "OTP Resent Successfully",
                "username": user_email,
                "contact_number": contact_number,
                "type": user_type,
                "sequence_no": sequence_no
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                "success": False,
                "message": "No Registered User Found"
            }, status=status.HTTP_400_BAD_REQUEST)

class SendotpView(APIView):
    permission_classes = [AllowAny]

    def generate_otp(self, length=4):
        """Generate a random numeric OTP"""
        return ''.join(random.choices(string.digits, k=length))

    def post(self, request):
        contactnumber = request.data.get("contactnumber")
        
        if not contactnumber:
            return Response({
                "success": False,
                "message": "Mobile Number is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check Student
        student = Student.objects.filter(contact_number=contactnumber).select_related('user').first()
        
        # Check Employee if not found in Employee
        employee = None
        if not student:
            employee = Employee.objects.filter(contact_number=contactnumber).select_related('user').first()

        if employee or student:
            # Generate OTP
            otp = self.generate_otp()
            otp = '1234'
            
            if employee:

                # Save OTP in database
                Onetimepassword.objects.create(
                    user_id=str(employee.user.email),
                    service="Login via OTP",
                    otp=otp,
                    sent_time=timezone.now(),
                    via_sms="1",
                    sequence_no="1"
                )

                return Response({
                    "success": True,
                    "message": "OTP Sent Successfully",
                    "username": employee.user.email,  # change to actual field in User model
                    "contact_number": employee.contact_number,
                    "type": "employee"
                }, status=status.HTTP_200_OK)

            elif student:

                # Save OTP in database
                Onetimepassword.objects.create(
                    user_id=str(student.user.email),
                    service="Login via OTP",
                    otp=otp,
                    sent_time=timezone.now(),
                    via_sms="1"
                )

                return Response({
                    "success": True,
                    "message": "OTP Sent Successfully",
                    "username": student.user.email,  # change to actual field in User model
                    "contact_number": student.contact_number,
                    "type": "student"
                }, status=status.HTTP_200_OK)

        else:
            return Response({
                "success": False,
                "message": "No Registered User Found"
            }, status=status.HTTP_400_BAD_REQUEST)


class GenerateotpView(APIView):
    permission_classes = [AllowAny]

    def generate_otp(self, length=4):
        """Generate a random numeric OTP"""
        return ''.join(random.choices(string.digits, k=length))

    def post(self, request):
        username = request.data.get("username")
        
        if not username:
            return Response({
                "success": False,
                "message": "Username is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Search in Employee table
        employee = Employee.objects.filter(user__email=username).select_related('user').first()

        # Search in Student if not found
        student = None
        if not employee:
            student = Student.objects.filter(user__email=username).select_related('user').first()

        if employee or student:
            if employee:
                user_obj = employee.user
                contact_number = employee.contact_number
                user_type = "employee"
            else:
                user_obj = student.user
                contact_number = student.contact_number
                user_type = "student"

            # Generate new OTP
            otp = self.generate_otp()
            otp = '1234'

            # Get last sequence_no for this user
            last_otp = Onetimepassword.objects.filter(user_id=username).order_by('-created_at').first()
            sequence_no = (last_otp.sequence_no + 1) if last_otp else 1

            # Save OTP in database
            Onetimepassword.objects.create(
                user_id=username,
                service="Passsord Reset",
                otp=otp,
                sent_time=timezone.now(),
                via_sms="1",
                sequence_no=sequence_no
            )

            return Response({
                "success": True,
                "message": "OTP sent successfully.",
                "username": username,
                "contact_number": contact_number,
                "otp": otp,
                "type": user_type,
                "sequence_no": sequence_no
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                "success": False,
                "message": "No registered user found with this username."
            }, status=status.HTTP_400_BAD_REQUEST)

class ValidateotpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        otp = request.data.get("otp")
        
        if not username or not otp:
            return Response({
                "success": False,
                "message": "Username and otp are required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate cutoff time (10 minutes ago)
        cutoff_time = timezone.now() - timedelta(minutes=10)

        # Check if OTP is valid and recent
        otp_entry = Onetimepassword.objects.filter(
            user_id=username,
            otp=otp,
            created_at__gte=cutoff_time
        ).order_by('-created_at').first()

        if otp_entry:

            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "No active account found for this email."
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            if user.status != User.Status.ACTIVE:
                return Response({
                    "success": False,
                    "message": "Account is not active."
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Calculate MD5 hash of username + created_at
            raw_string = f"{username}{user.created_at}"
            hash_value = hashlib.md5(raw_string.encode()).hexdigest()
            
            response = Response({
                "success": True,
                "message": "OTP Verified",
                "h": hash_value,
            },status=status.HTTP_200_OK)
            
            return response

        else:
            return Response({
                "success": False,
                "message": "Invalid or expired OTP."
            }, status=status.HTTP_400_BAD_REQUEST)

class SavepasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        repassword = request.data.get("repassword")
        h = request.data.get("h")
        
        if not username or not password or not repassword or not h:
            return Response({
                "success": False,
                "message": "Incomplete Data Received."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if password != repassword:
            return Response({
                "success": False,
                "message": "Password and Confirm Password should be same."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Fetch latest OTP entry for the username
        otp_entry = Onetimepassword.objects.filter(user_id=username).order_by('-created_at').first()

        if not otp_entry:
            return Response({
                "success": False,
                "message": "No OTP entry found for this username."
            }, status=status.HTTP_400_BAD_REQUEST)

        

        # Update user password
        try:
            user = User.objects.get(email=username)  # adjust if username is not email

            # Calculate MD5 hash of username + created_at
            raw_string = f"{username}{user.created_at}"
            calculated_hash = hashlib.md5(raw_string.encode()).hexdigest()

            if calculated_hash != h:
                return Response({
                    "success": False,
                    "message": "Invalid or expired link."
                }, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()
        except User.DoesNotExist:
            return Response({
                "success": False,
                "message": "User not found."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Password updated successfully."
        }, status=status.HTTP_200_OK)


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            
            if user.status != User.Status.ACTIVE:
                return Response({
                    "success": False,
                    "message": "Account is not active."
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Determine user type
            user_type = "other"
            if hasattr(user, 'employees') and user.employees.exists():
                user_type = "employee"
            elif hasattr(user, 'students') and user.students.exists():
                user_type = "student"
            
            return Response({
                "success": True,
                "message": "User details retrieved successfully!",
                "user": {
                    "email": user.email,
                    "contact_number": get_user_phone(user),
                    "country_code": get_user_country_code(user),
                    "name": get_user_name(user),
                    "photo_url": get_user_photo_url(user, request),
                    "status": user.status,
                    "device_token_key": user.device_token_key,
                    "user_type": user_type,
                }
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to retrieve user details: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GoogleLogin(APIView):
    permission_classes = [AllowAny]

    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request):
        try:
            print("Google login attempt received")

            token = request.data.get("credential") or request.data.get("id_token")
            device_token_key = request.data.get("device_token_key")
            # Get platform from request parameter, default to 'web' if not provided
            platform = request.data.get('platform', 'web')
            
            # automatic platform detection for future use
            # platform = detect_platform(request)

            # Fallback: form-encoded
            if not token:
                print("No token provided")
                return Response({
                    "success": False,
                    "message": "ID token is required."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            #print(f"Verifying token with client ID: {settings.GOOGLE_OAUTH_CLIENT_ID}")
            #print(f"Token length: {len(token) if token else 0}")
            
            if platform == 'android':
                # Use Android-specific client ID if configured, otherwise fall back to web client ID
                client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID_ANDROID', None)
                if client_id:
                    print(f"Using Android client ID: {client_id}")
                else:
                    client_id = settings.GOOGLE_OAUTH_CLIENT_ID
                    print(f"Android client ID not configured, using web client ID: {client_id}")
            elif platform == 'ios':
                # Use iOS-specific client ID if configured, otherwise fall back to web client ID
                client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID_IOS', None)
                if client_id:
                    print(f"Using iOS client ID: {client_id}")
                else:
                    client_id = settings.GOOGLE_OAUTH_CLIENT_ID
                    print(f"iOS client ID not configured, using web client ID: {client_id}")
            elif platform == 'mobile':
                # Fallback for generic mobile platform - use Android client ID if available
                client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID_ANDROID', None)
                if client_id:
                    print(f"Using Android client ID for mobile platform: {client_id}")
                else:
                    client_id = settings.GOOGLE_OAUTH_CLIENT_ID
                    print(f"Android client ID not configured for mobile platform, using web client ID: {client_id}")
            else:
                # Use the original web client ID for web platform or any other platform
                client_id = settings.GOOGLE_OAUTH_CLIENT_ID
                print(f"Using web client ID: {client_id}")
            
            if not client_id or not client_id.endswith('.apps.googleusercontent.com'):
                print("Warning: Client ID format looks incorrect")
            
            info = id_token.verify_oauth2_token(
                token, requests.Request(),
                client_id
            )
            print(f"Token verified successfully. User info: {info}")
            
            user, created = User.objects.get_or_create(
                email=info["email"],
                defaults={
                    "status": User.Status.ACTIVE,
                    "device_token_key": device_token_key,
                }
            )
            
            if created:
                create_user_profile(user, platform, info.get("name"))
            
            if not created and user.status != User.Status.ACTIVE:
                user.status = User.Status.ACTIVE
                user.save(update_fields=["status"])
            
            if not created and device_token_key:
                user.device_token_key = device_token_key
                user.save(update_fields=['device_token_key'])
            
            # Determine user type
            user_type = "other"
            if hasattr(user, 'employees') and user.employees.exists():
                user_type = "employee"
            elif hasattr(user, 'students') and user.students.exists():
                user_type = "student"
                
            refresh = RefreshToken.for_user(user)
            response = Response({
                "success": True,
                "message": "Google login successful!",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "email": user.email,
                    "contact_number": get_user_phone(user),
                    "country_code": get_user_country_code(user),
                    "name": get_user_name(user),
                    "photo_url": get_user_photo_url(user, request),
                    "status": user.status,
                    "device_token_key": user.device_token_key,
                    "user_type": user_type,
                },
                "next": "/",
            }, status=200)
            
            # Set cookies for backend authentication (30 days = 30 * 24 * 60 * 60 seconds)
            response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=False, samesite='Lax', max_age=2592000)
            response.set_cookie('refresh_token', str(refresh), httponly=True, secure=False, samesite='Lax', max_age=2592000)
            
            return response
            
        except ValueError as e:
            print(f"ValueError in Google login: {e}")
            return Response({
                "success": False,
                "message": f"Invalid Google token: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Exception in Google login: {e}")
            print(f"Exception type: {type(e)}")
            #import traceback
            #traceback.print_exc()
            return Response({
                "success": False,
                "message": f"Google authentication error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh") or request.COOKIES.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            response = Response({
                "success": True,
                "message": "Logged out successfully."
            })
            
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            
            return response
        except Exception:
            response = Response({
                "success": False,
                "message": "Invalid token."
            }, status=400)
            
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            
            return response

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            current_password = request.data.get("current_password")
            new_password = request.data.get("new_password")
            
            if not current_password or not new_password:
                return Response({
                    "success": False,
                    "message": "Current password and new password are required."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = request.user
            
            if not user.check_password(current_password):
                return Response({
                    "success": False,
                    "message": "Current password is incorrect."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
            
            return Response({
                "success": True,
                "message": "Password changed successfully!"
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to change password: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
