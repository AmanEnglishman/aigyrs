from django.db import models
from apps.users.models import MyUser
from PIL import Image
import os
from django.core.files.base import ContentFile
from io import BytesIO


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    )

    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')
    image = models.ImageField(upload_to='posts/%Y/%m/%d/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(MyUser, related_name='liked_posts', blank=True)
    location = models.CharField(max_length=100, blank=True)
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Пост {self.user.email} создан {self.created_at}'

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')  # на всякий случай

            # Изменяем размер, если нужно
            max_width = 1080
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)

            # Создаём буфер
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=80)
            buffer.seek(0)

            # Заменяем self.image на файл из буфера
            filename = os.path.basename(self.image.name)
            self.image.save(filename, ContentFile(buffer.read()), save=False)

            # Сохраняем размеры
            self.image_width = img.width
            self.image_height = img.height

        super().save(*args, **kwargs)
