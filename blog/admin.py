from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Series, Post, Comment, Link


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = '文章数量'


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'created_at', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['order']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = '文章数量'


class PostAdmin(admin.ModelAdmin):
    """文章管理后台"""
    list_display = ['title', 'author', 'category', 'status', 'featured', 'views', 'published_at', 'created_at']
    list_filter = ['status', 'category', 'tags', 'series', 'featured', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    ordering = ['-published_at', '-created_at']
    date_hierarchy = 'published_at'

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('分类与标签', {
            'fields': ('category', 'tags', 'series', 'series_order')
        }),
        ('内容', {
            'fields': ('excerpt', 'content', 'cover_image', 'gallery_images')
        }),
        ('特色设置', {
            'fields': ('featured', 'featured_order'),
            'classes': ('collapse',)
        }),
        ('统计', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.status == 'published' and not obj.published_at:
            from django.utils import timezone
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    """评论管理后台"""
    list_display = ['author_name', 'post', 'content_preview', 'is_approved', 'is_spam', 'created_at']
    list_filter = ['is_approved', 'is_spam', 'created_at']
    search_fields = ['author_name', 'author_email', 'content']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    actions = ['approve_comments', 'mark_as_spam', 'delete_spam']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '评论内容'

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = '批准选中的评论'

    def mark_as_spam(self, request, queryset):
        queryset.update(is_spam=True, is_approved=False)
    mark_as_spam.short_description = '标记为垃圾评论'

    def delete_spam(self, request, queryset):
        queryset.delete()
    delete_spam.short_description = '删除垃圾评论'


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', '-created_at']
