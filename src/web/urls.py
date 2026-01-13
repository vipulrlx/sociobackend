from django.urls import path, include
from .api.views import auth, employee, user, webview, dashboard, business, product, lead, elwebhook

app_name = "web"
urlpatterns = [
    # Main dashboard
    path("", dashboard.WebDashboardView.as_view(), name="dashboard"),
    
    # Authentication routes
    path("login/", auth.WebLoginView.as_view(), name="login"),
    path("register/", auth.WebRegisterView.as_view(), name="register"),
    path("logout/", auth.web_logout_view, name="logout"),
    path("change-password/", auth.WebChangePasswordView.as_view(), name="change_password"),
    
    # User routes
    path("users/", user.web_user_list_view, name="user_list"),
    
    # Employee routes
    path("create-employee/", employee.web_employee_create_view, name="create_employee"),
    path("employees/", employee.web_employee_list_view, name="employee_list"),
    path("employees/<int:employee_id>/", employee.web_employee_detail_view, name="employee_detail"),
    path("employees/<int:employee_id>/edit/", employee.web_employee_edit_view, name="employee_edit"),
    
    # API routes
    path("api/v1/getwebview1/", webview.Webview1View.as_view(), name="getwebview1"),

    # API business
    path("api/v1/business/", business.BusinessListCreateView.as_view(), name="addbusiness"),
    path('api/v1/business/<int:pk>/', business.BusinessRetrieveUpdateView.as_view(), name="updatebusiness"),

    # API product
    path("api/v1/product/", product.ProductListCreateView.as_view(), name="addproduct"),
    path('api/v1/product/<int:pk>/', product.ProductRetrieveUpdateView.as_view(), name="updateproduct"),

    #ElevelLab
    path('api/v1/webhook/elevenlabs/', elwebhook.ElevenLabsWebhookView.as_view(), name="elevellabs"),

    #Lead API
    path('api/v1/leads/', lead.LeadListView.as_view(), name="addleads"),
    path('api/v1/leads/<int:pk>/', lead.LeadDetailView.as_view(), name="updateleads"),   
]
