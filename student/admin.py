from django.contrib import admin
from .models import Post, Comment, Like, Room, Message

# Register your models here.
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Room)
admin.site.register(Message)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('text',), }
