import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Post

@receiver(post_delete, sender=Post)
def delete_image_file(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        try:
            os.remove(instance.image.path)
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")
