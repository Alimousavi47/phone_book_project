from rest_framework import serializers
from contacts_module.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    owner = serializers.ReadOnlyField(source='user.name')
    selected = serializers.BooleanField(default=False)
    class Meta:
        model = Contact
        fields = ['owner', 'id', 'name', 'phone_number', 'email', 'selected']
