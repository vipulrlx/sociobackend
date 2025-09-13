# Import views from grouped modules

from .api.views.auth import (
    WebLoginView as LoginView,
    WebRegisterView as RegisterView,
    WebChangePasswordView as ChangePasswordView,
    web_logout_view as logout_view
)

from .api.views.user import (
    web_user_list_view as user_list_view
)

from .api.views.webview import (
    Webview1View as Webview1View
)

from .api.views.employee import (
    web_employee_create_view as employee_create_view,
    web_employee_list_view as employee_list_view,
    web_employee_detail_view as employee_detail_view,
    web_employee_edit_view as employee_edit_view
)
