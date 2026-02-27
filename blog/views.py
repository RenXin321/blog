from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Category, Tag, Series, Comment, Link
from newsletter.models import Subscriber


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class HomeView(ListView):
    """首页视图"""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 特色文章（用于滑块）
        featured_posts = Post.objects.filter(
            status='published',
            featured=True
        ).select_related('author').order_by('featured_order', '-published_at')[:5]
        context['featured_posts'] = featured_posts

        # 热门标签
        context['popular_tags'] = Tag.objects.annotate(
            post_count=Count('posts')
        ).filter(post_count__gt=0).order_by('-post_count')[:15]

        # 文章分类
        context['categories'] = Category.objects.annotate(
            post_count=Count('posts')
        ).filter(post_count__gt=0).order_by('-post_count')

        # 友链
        context['links'] = Link.objects.filter(is_active=True).order_by('order')

        # 系列文章
        context['series_list'] = Series.objects.annotate(
            post_count=Count('posts')
        ).filter(post_count__gt=0).order_by('-post_count')[:5]

        return context


class PostListView(ListView):
    """文章列表视图"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')

        # 按年份筛选
        year = self.kwargs.get('year')
        if year:
            queryset = queryset.filter(published_at__year=year)

        # 按月份筛选
        month = self.kwargs.get('month')
        if month:
            queryset = queryset.filter(published_at__month=month)

        # 按分类筛选
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # 按标签筛选
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        # 按系列筛选
        series_slug = self.kwargs.get('series_slug')
        if series_slug:
            queryset = queryset.filter(series__slug=series_slug).order_by('series_order')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = self.kwargs.get('year')
        context['current_month'] = self.kwargs.get('month')
        context['current_category'] = self.kwargs.get('category_slug')
        context['current_tag'] = self.kwargs.get('tag_slug')
        context['current_series'] = self.kwargs.get('series_slug')
        return context


class PostDetailView(DetailView):
    """文章详情视图"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category', 'series').prefetch_related('tags', 'comments')

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        # 增加浏览量
        post.views += 1
        post.save(update_fields=['views'])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # 获取已审核的顶级评论
        comments = post.comments.filter(parent__isnull=True, is_approved=True).select_related().order_by('created_at')
        context['comments'] = comments
        context['comment_count'] = post.comments.filter(is_approved=True).count()

        # 系列中的其他文章
        if post.series:
            series_posts = post.series.posts.filter(status='published').order_by('series_order')
            context['series_posts'] = series_posts
            context['series_position'] = list(series_posts.values_list('id', flat=True)).index(post.id) + 1

        # 相关文章（相同分类）
        related_posts = Post.objects.filter(
            status='published',
            category=post.category
        ).exclude(id=post.id)[:4]
        context['related_posts'] = related_posts

        # 热门文章
        context['popular_posts'] = Post.objects.filter(
            status='published'
        ).order_by('-views')[:5]

        # 标签云
        context['all_tags'] = Tag.objects.annotate(
            post_count=Count('posts')
        ).filter(post_count__gt=0).order_by('-post_count')

        return context

    def post(self, request, *args, **kwargs):
        """处理评论提交"""
        post = self.get_object()

        author_name = request.POST.get('author_name', '').strip()
        author_email = request.POST.get('author_email', '').strip()
        author_url = request.POST.get('author_url', '').strip()
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')

        if not all([author_name, author_email, content]):
            messages.error(request, '请填写所有必填字段。')
            return redirect('blog:post_detail', slug=post.slug)

        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id, post=post)

        comment = Comment.objects.create(
            post=post,
            parent=parent,
            author_name=author_name,
            author_email=author_email,
            author_url=author_url,
            content=content,
            ip_address=get_client_ip(request),
            is_approved=False  # 需要审核
        )

        messages.success(request, '评论已提交，等待审核通过后显示。')
        return redirect('blog:post_detail', slug=post.slug)


class ArchiveView(ListView):
    """归档视图"""
    model = Post
    template_name = 'blog/archive.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category').order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']

        # 按年份分组
        posts_by_year = {}
        for post in posts:
            year = post.published_at.year
            if year not in posts_by_year:
                posts_by_year[year] = []
            posts_by_year[year].append(post)

        context['posts_by_year'] = posts_by_year

        # 所有年份
        context['years'] = sorted(posts_by_year.keys(), reverse=True)

        # 所有标签及文章数
        context['all_tags'] = Tag.objects.annotate(
            post_count=Count('posts')
        ).filter(post_count__gt=0).order_by('-post_count')

        # 所有系列
        context['all_series'] = Series.objects.annotate(
            post_count=Count('posts')
        ).filter(post_count__gt=0).order_by('-post_count')

        return context


class SearchView(ListView):
    """搜索结果视图"""
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query),
                status='published'
            ).select_related('author', 'category').prefetch_related('tags')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


def about(request):
    """关于页面"""
    context = {
        'popular_posts': Post.objects.filter(status='published').order_by('-views')[:5],
    }
    return render(request, 'blog/about.html', context)


@require_http_methods(["POST"])
def like_post(request):
    """点赞文章（简单实现）"""
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    # 这里可以添加更复杂的点赞逻辑
    return JsonResponse({'success': True, 'likes': post.views})
