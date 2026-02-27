from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
import markdown
from markdown.extensions import extra, codehilite, toc, footnotes


class Category(models.Model):
    """文章分类"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL别名')
    description = models.TextField(blank=True, verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField(max_length=50, verbose_name='标签名称')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL别名')
    color = models.CharField(max_length=20, default='#C5A059', verbose_name='标签颜色')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['name']

    def __str__(self):
        return self.name


class Series(models.Model):
    """文章系列"""
    name = models.CharField(max_length=100, verbose_name='系列名称')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL别名')
    description = models.TextField(blank=True, verbose_name='系列描述')
    cover_image = models.ImageField(upload_to='series/covers/', blank=True, verbose_name='封面图片')
    order = models.PositiveIntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '系列'
        verbose_name_plural = '系列'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name


class Post(models.Model):
    """博客文章"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]

    title = models.CharField(max_length=200, verbose_name='标题')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL别名')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name='分类')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True, verbose_name='标签')
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name='所属系列')
    series_order = models.PositiveIntegerField(default=0, verbose_name='系列内序号')

    excerpt = models.TextField(max_length=500, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文内容')
    content_html = models.TextField(blank=True, verbose_name='渲染后的HTML')

    featured = models.BooleanField(default=False, verbose_name='设为特色文章')
    featured_order = models.PositiveIntegerField(default=0, verbose_name='特色文章排序')

    cover_image = models.ImageField(upload_to='posts/covers/', blank=True, verbose_name='封面图片')
    gallery_images = models.JSONField(default=list, blank=True, verbose_name='画廊图片')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='发布状态')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 自动生成slug
        if not self.slug:
            self.slug = slugify(self.title)

        # 渲染Markdown内容
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc', 'footnotes'])
        self.content_html = md.convert(self.content)

        # 设置发布时间
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    """文章评论"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='父评论')
    author_name = models.CharField(max_length=50, verbose_name='评论者昵称')
    author_email = models.EmailField(verbose_name='评论者邮箱')
    author_url = models.URLField(blank=True, verbose_name='评论者网站')
    content = models.TextField(verbose_name='评论内容')
    is_approved = models.BooleanField(default=False, verbose_name='是否通过审核')
    is_spam = models.BooleanField(default=False, verbose_name='是否垃圾评论')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} 的评论: {self.content[:50]}...'

    @property
    def children(self):
        """获取子评论"""
        return Comment.objects.filter(parent=self, is_approved=True).order_by('created_at')


class Link(models.Model):
    """友链"""
    name = models.CharField(max_length=50, verbose_name='网站名称')
    url = models.URLField(verbose_name='网站地址')
    description = models.TextField(blank=True, verbose_name='网站描述')
    avatar = models.ImageField(upload_to='links/avatars/', blank=True, verbose_name='网站图标')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    order = models.PositiveIntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '友链'
        verbose_name_plural = '友链'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name
