from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import Menu
from ..serializers.menu import MenuSerializer, SubMenuSerializer

class MenuListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Get category from query parameters, default to 'web'
            category = request.query_params.get('category', 'web')
            
            # Get active menus with their submenus, filtered by category
            menus = Menu.objects.filter(
                is_active=True, 
                category=category
            ).prefetch_related('submenus').order_by('sequence')
            #print(f"Found {menus.count()} active menus for category: {category}")
            
            # Create a list to store menu data with filtered submenus
            menu_data = []
            for menu in menus:
                # Check if user has permission for this menu's destination_url
                menu_has_permission = True
                if menu.destination_url:
                    menu_has_permission = request.user.has_permission(menu.destination_url)
                
                # Get active submenus for this menu
                active_submenus = menu.submenus.filter(is_active=True).order_by('sequence')
                #print(f"Menu '{menu.display_name}' has {active_submenus.count()} active submenus")
                
                # Filter submenus based on user permissions
                permitted_submenus = []
                for submenu in active_submenus:
                    if submenu.destination_url:
                        if request.user.has_permission(submenu.destination_url):
                            permitted_submenus.append(submenu)
                    else:
                        # If no destination_url, include it (might be a parent menu)
                        permitted_submenus.append(submenu)

                # Only include menu if user has permission for menu URL or has permitted submenus
                if menu_has_permission or permitted_submenus:
                    # Serialize the menu
                    menu_serializer = MenuSerializer(menu)
                    menu_dict = menu_serializer.data
                    
                    # Replace submenus with only permitted ones
                    submenu_serializer = SubMenuSerializer(permitted_submenus, many=True)
                    menu_dict['submenus'] = submenu_serializer.data
                    
                    menu_data.append(menu_dict)
            
            response_data = {
                "success": True,
                "category": category,
                "menus": menu_data
            }
            return Response(response_data)
        except Exception as e:
            print(f"Error in MenuListView: {str(e)}")
            return Response({
                "success": False,
                "message": f"Failed to fetch menus: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 