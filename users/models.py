from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)  # Required and unique
    phone_number = models.CharField(max_length=15, unique=True)  # Optional: can enforce uniqueness
    date_of_birth = models.DateField(null=True, blank=True)  # Optional during registration

    USERNAME_FIELD = 'email'  # Use email for login instead of username
    REQUIRED_FIELDS = ['username']  # username is still required

    def __str__(self):
        return self.email

