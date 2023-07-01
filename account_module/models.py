import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
# from django.utils.timezone import now
from django.utils import timezone

# Create your models here.

class TimeModel(models.Model):
    # Common fields for all models
    # Field to store creation timestamp
    # Field to store last update timestamp
    created_at = models.DateTimeField(default=timezone.now,verbose_name='created at', editable=False) 
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='updated at') 

    class Meta:
        # Indicates that this is an abstract base class and won't create a separate table
        abstract = True 

    def save(self, *args, **kwargs):
        # Update the 'updated_at' field with the current timestamp
        # Call the original save() method of the parent class
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs) 


class User(AbstractUser, TimeModel):
    
    # If a field has blank=False, the field will be required.
    # If a field has blank=True, form validation will allow entry of an empty value.
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='name', db_index=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True, verbose_name='first_name')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='last_name')
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='account_users')
    user_permissions = models.ManyToManyField(
        Permission, verbose_name='user permissions', blank=True, related_name='account_users'
    )
    phone_number = models.CharField(max_length=20, verbose_name='phone nummber', blank=True)
    email = models.EmailField(max_length=300, unique=True, verbose_name='email', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='active / deactive', )
    is_delete = models.BooleanField(default=False, verbose_name='delete / not delete')
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email 
