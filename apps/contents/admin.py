from django.contrib import admin

from apps.contents.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('caption', 'user__email', 'location')
    readonly_fields = ('created_at', 'updated_at', 'image_width', 'image_height')