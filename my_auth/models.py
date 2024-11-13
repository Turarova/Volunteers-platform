from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        """Create and save a User with the given email, first_name, last_name, and password"""
        if not email:
            raise ValueError('User must have an email')
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        
        user = self.model(                     # self.model is the UserManager class
            email=self.normalize_email(email),  # normalize_email() is a helper function that converts email  1st to lowercase
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)  # change password to hash
        user.create_activation_code()
        user.save(using=self._db)  # save() is a helper function that saves the user to the database
        return user
    
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email=email, password=password, **extra_fields)
        

# Custom validator to check for at least one digit and Upper Letter in password        
def contains_digit_and_upperletter(value):
        if not any(char.isdigit() for char in value):
            raise ValidationError("This field must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise ValidationError("This field must contain at least one uppercase letter.")


class User(AbstractUser):

    username = None  # Remove the username fie
    email = models.EmailField(
        unique=True, 
        blank=False, 
        null=True, 
        verbose_name='Email',
        help_text="Enter an email address in format: email@domain.com.",
        error_messages={
            'unique': "A user with this email address already exists.",
        },)
    first_name = models.CharField(
        max_length=30,
        verbose_name="First Name"
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name="Last Name"
    )
    password = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(8), contains_digit_and_upperletter]

    )
    is_active = models.BooleanField('active', default=False)
    activation_code = models.CharField(max_length=36, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def create_activation_code(self):
        """Generates a unique activation code for the user"""
        code = str(uuid.uuid4())
        self.activation_code = code
        print(code)
    
    def activate_with_code(self, code):
        """Activate the user if the provided code matches the stored activation code"""
        if str(self.activation_code) != str(code):
            raise Exception(('Code does not match'))
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])

    





















    # Custom validator to check for at least one digit and Upper Letter
    # @staticmethod
    # def contains_digit_and_upperletter(value):
    #     if not any(char.isdigit() for char in value):
    #         raise ValidationError("This field must contain at least one digit.")
    #     if not any(char.isupper() for char in value):
    #         raise ValidationError("This field must contain at least one uppercase letter.")