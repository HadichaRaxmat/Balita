from django.contrib import admin
from .models import Post, Category, Comment, Contact


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'posts_count')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'view_count', 'comments_count', 'is_published', 'created_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Contact)
