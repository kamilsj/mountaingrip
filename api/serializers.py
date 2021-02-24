from rest_framework import serializers
from groups.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'user', 'name', 'description', 'pic')