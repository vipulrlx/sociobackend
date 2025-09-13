from django.shortcuts import render


def web_user_list_view(request):
    """Web user list view"""
    return render(request, 'web/user_list.html') 