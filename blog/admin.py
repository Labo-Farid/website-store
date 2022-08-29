from django.contrib import admin

from .models import Author, Category, Post, Comment, PostView


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'status', 'timestamp', 'author', 'is_on_top'
    ]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['author', 'categories', 'timestamp', 'country']
    ordering = ('author', 'status', 'timestamp', 'country')
    search_fields = ['title', 'content', 'categories', 'country']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostView)