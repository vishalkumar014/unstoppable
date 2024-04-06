from django.contrib import admin
from .models import *

class MusicAdmin(admin.ModelAdmin):
    list_display = ( 
        'id', 
        'title', 
        'content', 
        'duration', 
        'type', 
        'label',
        'cover', 
        'avatar', 
        'music',
        'video',
        'uuid', 
        'created_at',
        'updated_at', 
        'is_activate',
    )
admin.site.register(Music, MusicAdmin)


class SingerAdmin(admin.ModelAdmin):
    list_display = ( 
        'id', 
        'name', 
        'dob', 
        'details', 
        'social', 
        'avatar', 
        'uuid', 
        'tags',
        'created_at',
        'updated_at', 
        'is_activate', 
    )
admin.site.register(singer, SingerAdmin)


class PlayListAdmin(admin.ModelAdmin):
    list_display = ( 
        'id', 
        'user', 
        'title', 
        'content', 
        'cover', 
        'uuid', 
        'tags',
        'created_at',
        'updated_at', 
        'is_activate', 
    )
admin.site.register(PlayList, PlayListAdmin)
