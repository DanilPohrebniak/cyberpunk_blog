from django.contrib import admin

from blog.models import Post, Comment, CommentLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    ordering = ('-status', '-publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('author', 'body')

@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user')
    search_fields = ('user__username',)