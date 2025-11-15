from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Register(AbstractUser):
    usertype = models.CharField(max_length=10, default='admin')
    contact = models.CharField(max_length=10, null=True)
