from django.contrib import admin
from .models import Subscriber, Newsletter, NewsletterLog


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_verified', 'is_active', 'subscribe_date', 'last_sent_date']
    list_filter = ['is_verified', 'is_active', 'subscribe_date']
    search_fields = ['email', 'name']
    readonly_fields = ['token', 'subscribe_date', 'unsubscribe_date']
    ordering = ['-subscribe_date']

    actions = ['send_test_email', 'activate_subscribers']

    def send_test_email(self, request, queryset):
        # 发送测试邮件逻辑
        self.message_user(request, '测试邮件功能开发中...')
    send_test_email.short_description = '发送测试邮件'

    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True, is_verified=True)
    activate_subscribers.short_description = '激活选中的订阅者'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'status', 'recipient_count', 'open_count', 'scheduled_date', 'sent_date', 'created_at']
    list_filter = ['status', 'created_at', 'sent_date']
    search_fields = ['subject', 'content']
    readonly_fields = ['sent_date', 'recipient_count', 'open_count', 'created_at', 'updated_at']
    filter_horizontal = ['related_posts']

    fieldsets = (
        ('基本信息', {
            'fields': ('subject', 'content', 'content_html')
        }),
        ('关联文章', {
            'fields': ('related_posts',),
            'classes': ('collapse',)
        }),
        ('发送设置', {
            'fields': ('status', 'scheduled_date')
        }),
        ('统计', {
            'fields': ('recipient_count', 'open_count', 'sent_date'),
            'classes': ('collapse',)
        }),
    )

    actions = ['send_newsletter']

    def send_newsletter(self, request, queryset):
        for newsletter in queryset:
            if newsletter.status == 'draft':
                # 获取所有活跃订阅者
                subscribers = Subscriber.objects.filter(is_active=True, is_verified=True)
                newsletter.recipient_count = subscribers.count()
                newsletter.status = 'sent'
                newsletter.sent_date = timezone.now()
                newsletter.save()

                # 创建发送日志
                for subscriber in subscribers:
                    NewsletterLog.objects.create(
                        newsletter=newsletter,
                        subscriber=subscriber
                    )

                self.message_user(request, f'已发送新闻通讯 "{newsletter.subject}" 到 {newsletter.recipient_count} 位订阅者。')
    send_newsletter.short_description = '发送选中的新闻通讯'


@admin.register(NewsletterLog)
class NewsletterLogAdmin(admin.ModelAdmin):
    list_display = ['newsletter', 'subscriber', 'sent_date', 'opened', 'opened_date']
    list_filter = ['opened', 'sent_date']
    search_fields = ['newsletter__subject', 'subscriber__email']
    readonly_fields = ['sent_date', 'opened_date']
    date_hierarchy = 'sent_date'
