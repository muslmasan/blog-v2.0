from rest_framework import serializers
from .models import Post
import json
from django_quill.fields import QuillField

class QuillFieldSerializer(serializers.Field):
    """
    Serializer for django_quill's QuillField, storing the data as JSON.
    """
    def to_representation(self, value):
        # Converts the QuillField to a JSON representation when returning it in API responses
        return json.loads(value.json())

    def to_internal_value(self, data):
        # Validate that the input is a proper Quill Delta JSON structure
        if not isinstance(data, dict) or 'ops' not in data:
            raise serializers.ValidationError("Invalid format for Quill editor. Expecting a JSON object with 'ops'.")
        return data


class PostSerializer(serializers.ModelSerializer):
    body = QuillFieldSerializer()
    class Meta:
        model = Post
        fields = ['id', 'title','slug','body', 'created_at', 'updated_at','author',]
        read_only_fields = ['created_at', 'updated_at','author']

    def validate_body(self, value):
    # Assuming body is a Quill Delta JSON object
        if not isinstance(value, dict) or 'ops' not in value:
            raise serializers.ValidationError("Invalid body format for Quill.")
        return value
