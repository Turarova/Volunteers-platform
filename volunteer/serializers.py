from rest_framework import serializers
from django.contrib.auth import get_user_model
# from rest_framework.exceptions import ValidationError
# from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()


from rest_framework import serializers
from .models import User, Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания аккаунта (без ФИО и пароля)"""
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), required=False  # Делаем company необязательным
    )
    # company = serializers.ChoiceField(
    #     choices=[(company.name, company.name) for company in Company.objects.all()]
    # )
    is_manager = serializers.ChoiceField(choices=[('да', True), ('нет', False)], required=True)

    def validate_is_manager(self, value):
        if value == 'да':
            return True
        return False

    class Meta:
        model = User
        fields = ['id', 'is_manager', 'company']  # Не включаем ФИО и пароль
        read_only_fields = ['id']

    def validate(self, data):
        """Запрещает менеджерам передавать компанию вручную"""
        user = self.context['request'].user
        if user.is_manager and 'company' in data:
            raise serializers.ValidationError("Менеджеры не могут выбирать компанию!")
        return data

    def create(self, validated_data):
        company_name = validated_data.pop('company')
        company = Company.objects.get(name=company_name)
        return User.objects.create(company=company, **validated_data)


class CompleteRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для завершения регистрации (добавление ФИО и пароля)"""
    id = serializers.UUIDField(write_only=True)  # Вводимый код (ID)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']  

    def validate(self, data):
        """ Проверяем, что user существует и ещё не зарегистрирован """
        try:
            user = User.objects.get(id=data['id'])
            if any([user.first_name, user.last_name]):
                raise serializers.ValidationError("Пользователь уже зарегистрирован.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверный код.")
        return data
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exists')
        return value.lower().strip()

    def create(self, validated_data):
        """Сохраняем ФИО и хэшируем пароль"""
        user = User.objects.get(id=validated_data['id']) # Получаем существующего пользователя

        # Обновляем данные
        user.email = self.validate_email(validated_data['email'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.set_password(validated_data['password'])

        # Генерируем активационный код
        user.create_activation_code()

        user.save() # Сохраняем изменения
        return user

    # def update(self, instance, validated_data):
    #     """Сохраняем ФИО и хэшируем пароль"""
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.set_password(validated_data['password'])  
    #     instance.save()
    #     return instance

class ActivationSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True,
                                            write_only=True,
                                            max_length=255)


class DeleteUserSerializer(serializers.Serializer):
    """Сериализатор для удаления пользователя по email"""
    email = serializers.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем choices динамически с учетом всех пользователей в компании
        company_users = User.objects.filter(company=self.context['request'].user.company)
        self.fields['email'].choices = [(user.email, user.email) for user in company_users]


from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    """Кастомный логин по имени, фамилии и паролю"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields.pop('username')  # Убираем стандартное поле username
        self.fields['email'] = serializers.EmailField()

    def validate(self, attrs):
        """Проверяем first_name, last_name и password"""
        email = attrs.get("email")
        password = attrs.get("password")

        # Проверяем, переданы ли все поля
        if not password or not email:
            raise AuthenticationFailed("Email и пароль обязательны.")

        # try:
        #     # Ищем пользователя по имени и фамилии
        #     user = User.objects.get(email=email)
        # except User.DoesNotExist:
        #     raise AuthenticationFailed("Пользователь не найден.")

        # # Проверяем пароль
        # if not check_password(password, user.password):
        #     raise AuthenticationFailed("Неверный пароль.")

        # Аутентификация через встроенную Django-функцию
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Неверный email или пароль.")

        if not user.is_active:
            raise AuthenticationFailed("Пользователь не активирован.")

        # Генерируем токен
        data = super().validate({"email": email, "password": password})
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не существует.")
        return value


from django.contrib.auth.tokens import default_token_generator


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6)

    def validate_token(self, token):
        # ищем пользователя по токену
        user = self.get_user_from_token(token)
        if not user:
            raise serializers.ValidationError("Неверный или просроченный токен.")
        return user

    def get_user_from_token(self, token):
        try:
            # Попробуем получить ID пользователя с помощью токена
            uid = default_token_generator.check_token(token)
            if not uid:
                return None
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            return None
        except Exception:
            return None


































