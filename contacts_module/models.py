from django.db import models
from account_module.models import User
import uuid


class Contact(models.Model):
    # In your Contact model, you have specified related_name='contacts' for the user field.
    # This means that you can access the contacts belonging to a user
    # using user.contacts.all() instead of user.contact_set.all().
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts', verbose_name='contact user')
    name = models.CharField(max_length=100, verbose_name='name')
    phone_number = models.CharField(max_length=20, verbose_name='phone nummber')
    email = models.EmailField(max_length=300, unique=True, verbose_name='email')


    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'
        
    def __str__(self):
        return self.name
