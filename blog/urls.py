from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # 首页
    path('', views.HomeView.as_view(), name='home'),

    # 文章列表
    path('posts/', views.PostListView.as_view(), name='post_list'),

    # 文章详情
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),

    # 归档页面
    path('archive/', views.ArchiveView.as_view(), name='archive'),

    # 按年份归档
    path('archive/<int:year>/', views.PostListView.as_view(), name='archive_year'),
    path('archive/<int:year>/<int:month>/', views.PostListView.as_view(), name='archive_month'),

    # 按分类归档
    path('category/<slug:category_slug>/', views.PostListView.as_view(), name='category'),

    # 按标签归档
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='tag'),

    # 按系列归档
    path('series/<slug:series_slug>/', views.PostListView.as_view(), name='series'),

    # 搜索
    path('search/', views.SearchView.as_view(), name='search'),

    # 关于页面
    path('about/', views.about, name='about'),

    # 点赞
    path('like/', views.like_post, name='like_post'),
]
