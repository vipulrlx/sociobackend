from django.shortcuts import render


def web_employee_create_view(request):
    """Web employee create view"""
    return render(request, 'web/create-employee.html')


def web_employee_list_view(request):
    """Web employee list view"""
    return render(request, 'web/employee_list.html')


def web_employee_detail_view(request, employee_id):
    """Web employee detail view"""
    return render(request, 'web/employee_detail.html', {'employee_id': employee_id})


def web_employee_edit_view(request, employee_id):
    """Web employee edit view"""
    return render(request, 'web/edit-employee.html', {'employee_id': employee_id}) 