from django.db import models
from django.utils import timezone
import uuid


class Subscriber(models.Model):
    """新闻通讯订阅者"""
    email = models.EmailField(unique=True, verbose_name='邮箱地址')
    name = models.CharField(max_length=100, blank=True, verbose_name='昵称')
    token = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='验证令牌')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    is_verified = models.BooleanField(default=False, verbose_name='是否已验证')
    subscribe_date = models.DateTimeField(auto_now_add=True, verbose_name='订阅时间')
    unsubscribe_date = models.DateTimeField(null=True, blank=True, verbose_name='退订时间')
    last_sent_date = models.DateTimeField(null=True, blank=True, verbose_name='上次发送时间')

    class Meta:
        verbose_name = '订阅者'
        verbose_name_plural = '订阅者'
        ordering = ['-subscribe_date']

    def __str__(self):
        return self.email

    def unsubscribe(self):
        """退订"""
        self.is_active = False
        self.unsubscribe_date = timezone.now()
        self.save()


class Newsletter(models.Model):
    """新闻通讯"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('scheduled', '定时发送'),
        ('sent', '已发送'),
    ]

    subject = models.CharField(max_length=200, verbose_name='邮件主题')
    content = models.TextField(verbose_name='邮件内容')
    content_html = models.TextField(blank=True, verbose_name='HTML内容')

    # 关联的文章（可选）
    related_posts = models.ManyToManyField('blog.Post', blank=True, verbose_name='关联文章')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    scheduled_date = models.DateTimeField(null=True, blank=True, verbose_name='定时发送时间')
    sent_date = models.DateTimeField(null=True, blank=True, verbose_name='发送时间')

    recipient_count = models.PositiveIntegerField(default=0, verbose_name='接收者数量')
    open_count = models.PositiveIntegerField(default=0, verbose_name='打开数量')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '新闻通讯'
        verbose_name_plural = '新闻通讯'
        ordering = ['-created_at']

    def __str__(self):
        return self.subject


class NewsletterLog(models.Model):
    """发送日志"""
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name='logs', verbose_name='新闻通讯')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='logs', verbose_name='订阅者')
    sent_date = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    opened = models.BooleanField(default=False, verbose_name='是否打开')
    opened_date = models.DateTimeField(null=True, blank=True, verbose_name='打开时间')

    class Meta:
        verbose_name = '发送日志'
        verbose_name_plural = '发送日志'
        ordering = ['-sent_date']

    def __str__(self):
        return f'{self.newsletter.subject} -> {self.subscriber.email}'
