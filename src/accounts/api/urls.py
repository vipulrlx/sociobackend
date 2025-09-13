from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from .views.auth import RegisterView, CustomLoginView, GoogleLogin, LogoutView, ChangePasswordView, UserDetailsView, CategoryView, LoginotpView, SendotpView, ResendotpView, ValidateotpView, GenerateotpView, SavepasswordView
from .views.employee import EmployeeCreateView, EmployeeListView, EmployeeDetailView, EmployeeUpdateView, EmployeeDeleteView
from .views.menu import MenuListView
from .views.permissions import UserPermissionsView, CheckPermissionView
from .views.user import user_list_view, role_list_view, assign_role_view

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", CustomLoginView.as_view(), name="token_obtain_pair"),
    path("auth/loginviaotp/", LoginotpView.as_view(), name="loginviaotp"),
    path("auth/generateotp/", GenerateotpView.as_view(), name="generateotp"),
    path("auth/validateotp/", ValidateotpView.as_view(), name="validateotp"),
    path("auth/savepassword/", SavepasswordView.as_view(), name="savepassword"),
    path("auth/sendotp/", SendotpView.as_view(), name="sendotp"),
    path("auth/resendotp/", ResendotpView.as_view(), name="resendotp"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("auth/categorylist/", CategoryView.as_view(), name="category_list"),
    path("user/details/", UserDetailsView.as_view(), name="user_details"),
    path("menu/list/", MenuListView.as_view(), name="menu_list"),
    path("employee/create/", EmployeeCreateView.as_view(), name="employee_create"),
    path("employee/list/", EmployeeListView.as_view(), name="employee_list"),
    path("employee/<int:employee_id>/", EmployeeDetailView.as_view(), name="employee_detail"),
    path("employee/<int:employee_id>/update/", EmployeeUpdateView.as_view(), name="employee_update"),
    path("employee/<int:employee_id>/delete/", EmployeeDeleteView.as_view(), name="employee_delete"),
    path("permissions/user/", UserPermissionsView.as_view(), name="user_permissions"),
    path("permissions/check/", CheckPermissionView.as_view(), name="check_permission"),
    path("user/list/", user_list_view, name="user_list"),
    path("role/list/", role_list_view, name="role_list"),
    path("user/<int:user_id>/assign-role/", assign_role_view, name="assign_role"),
]
