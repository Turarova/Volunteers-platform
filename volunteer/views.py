from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
# from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from .helpers import *
from .serializers import *
from .permissions import *


class CompanyCreateView(GenericAPIView):
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Компания создана"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CreateUserView(CreateAPIView):
    """Создает учетную запись для менеджера или волонтера (без ФИО и пароля)"""
    serializer_class = UserCreateSerializer  
    permission_classes = [permissions.IsAdminUser | IsManagerPermission]

    def perform_create(self, serializer):
        """Принудительно назначаем компанию менеджеру"""
        user = self.request.user  # Текущий авторизованный пользователь

        if user.is_manager and not user.is_staff:
            # Менеджеры могут создавать только пользователей своей компании
            serializer.save(company=user.company)
        else:
            # Админ может назначать любую компанию
            serializer.save()
    
    def create(self, request, *args, **kwargs):
        """Добавляем возврат ID нового пользователя"""
        response = super().create(request, *args, **kwargs)

        id = response.data['id']
        # Определяем роль
        role = "Manager" if response.data['is_manager'] else "Volunteer"
            
        # Возвращаем ID и роль в ответе
        return Response({"id": id, "role": role}, status=status.HTTP_201_CREATED)
        


class CompleteRegistrationView(GenericAPIView):
    serializer_class = CompleteRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_confirmation_email(user.email, user.activation_code)
            return Response({"message": "Регистрация пользователя завершена."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationView(GenericAPIView):
    serializer_class = ActivationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.validated_data['activation_code']
            user = get_object_or_404(User, activation_code=code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg':'User successfully activated'})


class DeleteUserAPIView(GenericAPIView):
    """Удаление пользователя по выбору email"""

    permission_classes = [IsAuthenticated, IsManagerOfCompanyPermission]
    serializer_class = DeleteUserSerializer

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем email из выбранного пользователя
        email = serializer.validated_data['email']
        
        # Ищем пользователя по email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Удаляем пользователя
        user.delete()
        return Response({"detail": f"User {user.first_name} {user.last_name} with email {email} has been deleted."}, status=status.HTTP_204_NO_CONTENT)



class CustomTokenObtainPairView(TokenObtainPairView):
    """Кастомный логин по email + first_name + last_name + password"""
    serializer_class = CustomTokenObtainPairSerializer



class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({"msg":"You successfully logged out"}, status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestAPIView(APIView):
    """Запрос на сброс пароля"""
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Логика отправки письма с ссылкой на сброс пароля
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь с таким email не существует."}, status=status.HTTP_400_BAD_REQUEST)
        # Генерация токена
        token = default_token_generator.make_token(user)
        
        # Формирование ссылки для сброса пароля
        reset_url = f"http://your-frontend-url/reset-password/{token}/"
        
        # Отправка ссылки на email пользователя
        send_mail(
            "Сброс пароля",
            f"Перейдите по следующей ссылке для восстановления пароля: {reset_url}",
            "noreply@example.com",
            [email],
        )

        return Response({"detail": "Ссылка для восстановления пароля отправлена на ваш email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        # Уже в сериализаторе проверили токен и получили пользователя
        user = serializer.validated_data['user']  # Получаем пользователя, если токен валиден

        # Устанавливаем новый пароль
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Пароль успешно сброшен."}, status=status.HTTP_200_OK)