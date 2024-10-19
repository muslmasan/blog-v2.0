from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_quill.fields import QuillField
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    body = QuillField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Post)
def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
