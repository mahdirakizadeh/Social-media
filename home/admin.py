from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'update')
    search_fields = ('slug', 'body')
    list_filter = ('created',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)


admin.site.register(Comment)
