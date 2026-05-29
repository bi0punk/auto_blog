from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'magnitude', 'depth_km', 'utc_time', 'created_at']
    list_filter = ['magnitude', 'created_at']
    search_fields = ['title', 'location']
    date_hierarchy = 'created_at'
