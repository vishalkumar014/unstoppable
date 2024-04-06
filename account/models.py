from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted  = models.BooleanField(default=True)
    class Meta:
        abstract = True


class User(AbstractUser):
    dob             = models.CharField(max_length=15, blank=True, null=True)
    phone_number    = models.CharField(max_length=15, blank=True, null=True)
    avatar          = models.ImageField(upload_to='avatar/', blank=True, null=True)
    uuid            = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    otp             = models.CharField(max_length=300,blank=True, null=True)
    token           = models.CharField(max_length=300,blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)



