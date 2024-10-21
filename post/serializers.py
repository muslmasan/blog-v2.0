import base64
import re
from django.core.files.base import ContentFile
from django.utils.html import escape
from rest_framework import serializers
from .models import Post
import bleach

class QuillHTMLImageFieldSerializer(serializers.Field):
    """
    Serializer for handling HTML content from Quill editor, including embedded base64 images.
    """

    def to_representation(self, value):
        # Return the stored HTML as-is
        return str(value)

    def to_internal_value(self, data):
        # Ensure the data is a valid HTML string
        if not isinstance(data, str):
            raise serializers.ValidationError("Invalid format for Quill editor. Expecting an HTML string.")

        # Optionally sanitize HTML to avoid XSS
        clean_data = bleach.clean(data, tags=['b', 'i', 'a', 'p', 'h1', 'h2', 'strong', 'em', 'img'], attributes={'a': ['href'], 'img': ['src', 'alt']})

        # Process any base64 images and store them
        clean_data = self._handle_images(clean_data)

        return clean_data

    def _handle_images(self, html_content):
        """
        Extracts base64 images, saves them to the media directory, and replaces them with URLs in the HTML content.
        """
        # Regex to find base64 encoded images
        base64_pattern = r'data:image/(?P<ext>[^;]+);base64,(?P<data>[^"]+)'

        def replace_base64_with_url(match):
            ext = match.group('ext')  # Get the image file extension (e.g., png, jpg)
            data = match.group('data')  # Get the base64-encoded image data

            # Decode the image
            image_data = base64.b64decode(data)
            file_name = f"image_{int(time.time())}.{ext}"
            image_file = ContentFile(image_data, name=file_name)

            # Save the image file (this example assumes you have a function to save the image)
            saved_url = self._save_image(image_file)

            # Return the URL to replace the base64 image
            return saved_url

        # Replace all base64-encoded images in the HTML with actual URLs
        html_content_with_urls = re.sub(base64_pattern, replace_base64_with_url, html_content)

        return html_content_with_urls

    def _save_image(self, image_file):
        """
        Save the image file to the media directory and return the URL.
        """
        # Assuming your Post model has an 'images' field or you have some media storage logic
        # You can use default Django FileField save functionality, or any media storage service like S3.
        # For this example, save the image to a media directory.
        from django.core.files.storage import default_storage
        image_path = default_storage.save(f"media/images/{image_file.name}", image_file)

        # Return the publicly accessible URL of the saved image
        return f"/media/images/{image_file.name}"


class PostSerializer(serializers.ModelSerializer):
    body = QuillHTMLImageFieldSerializer()  # Updated to handle HTML with images

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'body', 'created_at', 'updated_at', 'author']
        read_only_fields = ['created_at', 'updated_at', 'author']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user  # Set the author to the current user
        return super().create(validated_data)
    def validate_body(self, value):
        # Additional custom validation for the HTML body can be added here
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise serializers.ValidationError("The body field must contain valid HTML content.")

        return value
