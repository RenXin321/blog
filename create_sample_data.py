#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from blog.models import Category, Tag, Series, Post
from django.contrib.auth import get_user_model

User = get_user_model()
admin = User.objects.get(username='admin')

# 创建分类
cat1 = Category.objects.create(name='Python', slug='python', description='Python相关技术文章')
cat2 = Category.objects.create(name='Django', slug='django', description='Django Web框架')
cat3 = Category.objects.create(name='前端开发', slug='frontend', description='HTML, CSS, JavaScript')

# 创建标签
tags = []
for name, slug, color in [
    ('Python', 'python', '#3572A5'),
    ('Django', 'django', '#092E20'),
    ('Web', 'web', '#C5A059'),
    ('教程', 'tutorial', '#FBCFE8'),
    ('进阶', 'advanced', '#E0F2FE')
]:
    tags.append(Tag.objects.create(name=name, slug=slug, color=color))

# 创建系列
series1 = Series.objects.create(
    name='Python进阶之路',
    slug='python-advanced',
    description='Python进阶系列教程',
    order=1
)
series2 = Series.objects.create(
    name='Django实战',
    slug='django-practice',
    description='Django项目实战',
    order=2
)

# 创建文章
posts_data = [
    {
        'title': 'Python入门指南：从零开始学习Python编程',
        'slug': 'python-getting-started',
        'excerpt': '本文将带你从零开始学习Python编程，了解Python的基本语法和核心概念。',
        'content': '''# Python入门指南

Python是一种简洁、优雅的编程语言，非常适合初学者入门。本文将介绍Python的基本语法和数据类型。

## 变量和数据类型

Python中的变量不需要声明类型，直接赋值即可：

```python
name = "樱花少女"
age = 18
height = 165.5
is_student = True
```

## 基本数据结构

### 列表
列表是Python中最常用的数据结构之一：

```python
fruits = ["苹果", "香蕉", "橘子"]
fruits.append("葡萄")
print(fruits)
```

### 字典
字典用于存储键值对：

```python
person = {"name": "小明", "age": 20}
print(person["name"])
```

## 结论

Python的语法简洁明了，非常适合编程初学者。
''',
        'featured': True,
        'featured_order': 1,
        'category': cat1
    },
    {
        'title': 'Django框架详解：构建现代化的Web应用',
        'slug': 'django-framework-detailed',
        'excerpt': '深入了解Django框架的核心概念和组件，学习如何构建现代化的Web应用。',
        'content': '''# Django框架详解

Django是一个高级Python Web框架，鼓励快速开发和简洁实用的设计。

## Django的核心组件

### URL路由
Django的URL路由系统非常灵活：

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
```

### 模型
Django的ORM系统让数据库操作变得简单：

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### 视图
视图处理业务逻辑：

```python
from django.shortcuts import render

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})
```

## Django的优势

1. **MTV架构** - 清晰的代码组织
2. **ORM** - 强大的数据库操作
3. **Admin后台** - 自动生成管理界面
4. **安全性** - 内置多种安全防护
''',
        'featured': True,
        'featured_order': 2,
        'category': cat2
    },
    {
        'title': '前端开发基础：HTML、CSS、JavaScript入门',
        'slug': 'frontend-basics',
        'excerpt': '学习前端开发的基础知识，掌握HTML、CSS和JavaScript的核心概念。',
        'content': '''# 前端开发基础

前端开发是Web开发的重要组成部分，本文介绍HTML、CSS和JavaScript的基础知识。

## HTML基础

HTML是网页的结构基础：

```html
<!DOCTYPE html>
<html>
<head>
    <title>我的网页</title>
</head>
<body>
    <h1>欢迎来到樱花博客</h1>
    <p>这是一个示例段落</p>
</body>
</html>
```

## CSS样式

CSS用于美化网页：

```css
body {
    font-family: 'Noto Sans SC', sans-serif;
    background-color: #FFFBF5;
    color: #374151;
}

h1 {
    color: #C5A059;
}
```

## JavaScript交互

JavaScript为网页添加交互：

```javascript
document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成！');
});
```
''',
        'featured': False,
        'category': cat3
    },
    {
        'title': 'RESTful API设计与实现',
        'slug': 'restful-api-design',
        'excerpt': '学习如何设计和实现RESTful风格的API接口。',
        'content': '''# RESTful API设计与实现

REST（Representational State Transfer）是一种常用的Web服务架构风格。

## RESTful原则

1. **统一接口** - 使用标准的HTTP方法
2. **无状态** - 每个请求包含所有必要信息
3. **分层系统** - 客户端不需要知道服务器细节

## HTTP方法对应

| 方法 | 说明 |
|------|------|
| GET | 获取资源 |
| POST | 创建资源 |
| PUT | 更新资源 |
| DELETE | 删除资源 |

## 示例

```python
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```
''',
        'featured': True,
        'featured_order': 3,
        'category': cat2
    },
]

for i, post_data in enumerate(posts_data):
    post = Post.objects.create(
        title=post_data['title'],
        slug=post_data['slug'],
        author=admin,
        category=post_data['category'],
        excerpt=post_data['excerpt'],
        content=post_data['content'],
        featured=post_data.get('featured', False),
        featured_order=post_data.get('featured_order', 0),
        status='published'
    )
    post.tags.set(tags[:3])
    if i < 2:
        post.series = series1
    else:
        post.series = series2
    post.save()

print('Sample data created successfully!')
print(f'Categories: {Category.objects.count()}')
print(f'Tags: {Tag.objects.count()}')
print(f'Series: {Series.objects.count()}')
print(f'Posts: {Post.objects.count()}')
