from django.contrib import admin

from .models import *


class VideoAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'status', 'timestamp', 'artist'
    ]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['artist', 'category', 'timestamp']
    ordering = ('artist', 'status', 'timestamp')
    search_fields = ['title', 'description', 'category']


class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(VideoView)
