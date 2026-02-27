from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.conf import settings
from .models import Subscriber, Newsletter, NewsletterLog
import uuid


@require_http_methods(["GET", "POST"])
def subscribe(request):
    """订阅新闻通讯"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()

        if not email:
            messages.error(request, '请输入邮箱地址。')
            return render(request, 'newsletter/subscribe.html')

        # 检查是否已存在
        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={'name': name}
        )

        if not created:
            if subscriber.is_active:
                messages.info(request, '您已经订阅过了！')
            else:
                # 重新激活
                subscriber.is_active = True
                subscriber.is_verified = False
                subscriber.token = uuid.uuid4()
                subscriber.save()
                send_verification_email(subscriber)
                messages.success(request, '请查收邮箱进行验证。')
        else:
            # 发送验证邮件
            send_verification_email(subscriber)
            messages.success(request, '订阅成功！请查收邮箱进行验证。')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': '订阅成功！请查收邮箱进行验证。'})

        return render(request, 'newsletter/subscribe_success.html')

    return render(request, 'newsletter/subscribe.html')


def verify_email(request, token):
    """验证邮箱"""
    subscriber = get_object_or_404(Subscriber, token=token)
    subscriber.is_verified = True
    subscriber.save()

    messages.success(request, '邮箱验证成功！您现在可以收到我们的新闻通讯了。')
    return redirect('blog:home')


@require_http_methods(["GET", "POST"])
def unsubscribe(request, token=None):
    """退订新闻通讯"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.unsubscribe()
            messages.success(request, '您已成功退订新闻通讯。')
        except Subscriber.DoesNotExist:
            messages.error(request, '该邮箱未订阅。')
        return redirect('blog:home')

    if token:
        subscriber = get_object_or_404(Subscriber, token=token)
        subscriber.unsubscribe()
        messages.success(request, '您已成功退订新闻通讯。')
        return redirect('blog:home')

    return render(request, 'newsletter/unsubscribe.html')


def send_verification_email(subscriber):
    """发送验证邮件"""
    verify_url = f"{settings.SITE_URL}/newsletter/verify/{subscriber.token}/"

    subject = '【樱花技术博客】邮箱验证'
    message = f'''
    您好 {subscriber.name or '朋友'}！

    感谢您订阅樱花技术博客！

    请点击以下链接验证您的邮箱：
    {verify_url}

    如果您没有订阅过我们的博客，请忽略此邮件。

    ---
    樱花技术博客
    '''

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"发送邮件失败: {e}")


def newsletter_management(request):
    """新闻通讯管理页面（仅管理员）"""
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面。')
        return redirect('blog:home')

    subscribers = Subscriber.objects.all()
    newsletters = Newsletter.objects.all()

    context = {
        'subscribers': subscribers,
        'newsletters': newsletters,
        'total_subscribers': Subscriber.objects.filter(is_active=True, is_verified=True).count(),
    }
    return render(request, 'newsletter/management.html', context)
