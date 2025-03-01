from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

import uuid



class Company(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Companies"



from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, last_name, password=None, is_manager=False, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name, 
            last_name=last_name, 
            is_manager=is_manager,  
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_manager", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)
    
def generate_temp_email():
    return f"temp_{uuid.uuid4().hex[:8]}@example.com" 

class User(AbstractUser):
    username = None  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        unique=True, 
        blank=True, 
        null=True,
        default=generate_temp_email, 
        verbose_name='Email',
        help_text="Enter an email address in format: email@domain.com.",
        error_messages={
            'unique': "A user with this email address already exists.",
        },)  
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_manager = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True)  
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=36, blank=True)
    company = models.ForeignKey(Company, related_name='users', on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        role = "Manager" if self.is_manager else "Volunteer"
        return f"{self.first_name} {self.last_name} ({role})"
    
    def create_activation_code(self):
        """Generates a unique activation code for the user"""
        code = str(uuid.uuid4())
        self.activation_code = code
        self.save(update_fields=['activation_code'])  
        print("Activation code=> ", code)
    
    def activate_with_code(self, code):
        """Activate the user if the provided code matches the stored activation code"""
        if str(self.activation_code) != str(code):
            raise Exception(('Code does not match'))
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])