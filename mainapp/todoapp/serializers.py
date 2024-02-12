from rest_framework import serializers
from .models import Todo
import bleach
class TodoSerializer(serializers.ModelSerializer):
    def validate_description(self, value):

        clean_value = bleach.clean(value)
        return clean_value
    class Meta:
        model = Todo
        fields = '__all__'