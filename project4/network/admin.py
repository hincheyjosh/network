from django.contrib import admin

from network.models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp", "total_likes")

admin.site.register(Post, PostAdmin)
admin.site.register(User)
admin.site.register(Follow)