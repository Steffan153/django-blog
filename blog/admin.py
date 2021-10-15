from django.contrib.admin.decorators import register
from django.contrib.admin.options import ModelAdmin
from .models import Author, Comment, Post, Tag

@register(Post)
class PostAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_filter = ('author', 'tags')
    search_fields = ('title', 'author', 'get_tags')
    list_display = ('title', 'author', 'date', 'get_tags')

    def get_tags(self, obj):
        return ', '.join(x.caption for x in obj.tags.all())

@register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = ('__str__', 'email')

@register(Tag)
class TagAdmin(ModelAdmin):
    pass

@register(Comment)
class CommentAdmin(ModelAdmin):
    list_filter = ('user_name', 'user_email', 'post')
    search_fields = ('user_name', 'user_email')
    list_display = ('user_name', 'user_email', 'post')