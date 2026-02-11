from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    national_code = models.CharField(max_length=10)

    def __str__(self):
        return self.national_code

class Author2(Author):
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    class Meta:
        proxy = True

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    is_author = models.BooleanField(default=False)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username or self.email or str(self.id)