from django.contrib import admin

from .models import Blog, Blogger, Comment


@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('username', 'bio')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'blogger', 'publication_request', 'is_posted', 'post_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'content', 'post_date', 'is_posted']
