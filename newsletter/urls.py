from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    # 订阅
    path('subscribe/', views.subscribe, name='subscribe'),

    # 验证邮箱
    path('verify/<uuid:token>/', views.verify_email, name='verify_email'),

    # 退订
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('unsubscribe/<uuid:token>/', views.unsubscribe, name='unsubscribe_token'),

    # 管理页面
    path('manage/', views.newsletter_management, name='manage'),
]
