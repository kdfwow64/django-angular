"""User manager to enable email instead of username."""
from django.contrib.auth.models import BaseUserManager
# from django.utils import timezone


class EmailUserManager(BaseUserManager):
    """The user manager."""

    def create_user(self, email, full_name, password=None, **extra_fields):
        """Create user override."""
        # today = timezone.now()

        if not email:
            raise ValueError('The given email address must be set')
        email = EmailUserManager.normalize_email(email)

        if not full_name:
            raise ValueError('You must provide a name for your account')

        user = self.model(email=email, full_name=full_name,
                          is_staff=False, is_active=True, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password, **extra_fields):
        """Create super user override."""
        u = self.create_user(email, full_name, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u
