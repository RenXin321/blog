# NEXUS BLOG - 个人技术博客

一个基于 Python (Django) 构建的现代化个人技术博客系统，采用科幻赛博朋克风格设计。

## 功能特性

- **特色文章滑块** - 支持动态排序的精选文章展示
- **富媒体文章** - 支持脚注、引文、画廊和丰富媒体内容
- **线程化评论** - 带有审核工具的评论系统
- **归档浏览** - 按年份、标签、系列筛选文章
- **新闻通讯** - 邮件订阅与管理系统
- **响应式设计** - 支持各种设备访问

## 技术栈

- **后端**: Python 3.x, Django 3.2+
- **数据库**: SQLite (开发环境) / PostgreSQL (生产环境)
- **前端**: HTML5, CSS3, JavaScript
- **字体**: Orbitron, Rajdhani, Inter, JetBrains Mono

## 项目结构

```
nexus-blog/
├── blog/                 # Django 博客应用
├── blog_project/         # Django 项目配置
├── newsletter/          # 新闻通讯应用
├── templates/           # HTML 模板
├── static/             # 静态文件
├── public/             # Vercel 部署静态文件 ⭐
├── dist/               # 备用静态文件
├── vercel.json        # Vercel 配置文件 ⭐
├── runtime.txt         # Python 版本 ⭐
└── requirements.txt    # Python 依赖
```

## 本地开发

### 1. 克隆项目

```bash
git clone https://github.com/your-username/nexus-blog.git
cd nexus-blog
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行迁移

```bash
python manage.py migrate
```

### 5. 创建管理员

```bash
python manage.py createsuperuser
```

### 6. 启动服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000 查看博客。

---

## 部署到 Vercel（推荐）

本项目已配置 Vercel 部署，只需简单几步即可上线：

### 步骤 1：推送代码到 GitHub

```bash
# 添加远程仓库（替换为您的 GitHub 用户名）
git remote add origin https://github.com/your-username/nexus-blog.git

# 推送代码
git push -u origin master
```

### 步骤 2：在 Vercel 导入项目

1. 访问 [Vercel](https://vercel.com) 并登录
2. 点击 **"New Project"**
3. 选择 **"Import Project"**
4. 选择刚刚推送的 GitHub 仓库
5. Vercel 会自动检测为静态网站部署
6. 点击 **"Deploy"** 开始部署

### 步骤 3：绑定自定义域名（可选）

部署完成后：
1. 进入项目设置 **"Settings"** → **"Domains"**
2. 添加您的域名（如 yourdomain.com）
3. 按照提示配置 DNS 解析

---

## 部署文件说明

### public/ 文件夹

包含已构建的静态 HTML 文件，直接部署到 Vercel：

- `index.html` - 首页
- `posts.html` - 文章列表
- `post-detail.html` - 文章详情
- `archive.html` - 归档页面
- `about.html` - 关于页面
- `_redirects` - 路由重定向配置

### vercel.json

Vercel 配置文件，指定静态文件部署：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "public/**",
      "use": "@vercel/static"
    }
  ]
}
```

### runtime.txt

指定 Python 版本：

```
python-3.11.0
```

---

## 许可证

MIT License

## 在线预览

- **Vercel 部署**: https://your-project.vercel.app
- **备用预览**: https://kdf08pg0owud.space.minimax.io
