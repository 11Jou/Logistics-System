
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserManager(BaseUserManager):


    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('Invalid email address')
    
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        self.validate_email(email)
        email = self.normalize_email(email)
        user = self.model(email=email,full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', "manager")
        user = self.create_user(email, full_name, password, **extra_fields)
        user.save(using=self._db)
        return user