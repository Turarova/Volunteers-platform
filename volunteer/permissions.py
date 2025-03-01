from rest_framework.permissions import BasePermission
from .models import User
from rest_framework.exceptions import PermissionDenied

class IsManagerPermission(BasePermission):
    """
    Разрешение для менеджеров.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager

    


class IsManagerOfCompanyPermission(BasePermission):
    """
    Разрешение для проверки, что пользователь является менеджером своей компании.
    """
    def has_permission(self, request, view):
        # Проверяем, является ли пользователь менеджером
        if not request.user.is_manager:
            return False
        
        # Если пользователь является менеджером, проверяем, что удаляемый пользователь
        # принадлежит его компании
        email = request.data.get('email')
        if not email:
            raise PermissionDenied("Email не был передан.")
        
        try:
            user_to_delete = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(f"Пользователь с email {email} не найден.")
        
        if user_to_delete.company != request.user.company:
            raise PermissionDenied(f"Пользователь с email {email} не принадлежит вашей компании.")

        return True 


