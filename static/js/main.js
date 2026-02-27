/**
 * 樱花技术博客 - 主JavaScript文件
 */

document.addEventListener('DOMContentLoaded', function() {
    // 移动菜单
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.getElementById('navMenu');

    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            const icon = this.querySelector('i');
            if (navMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // 特色文章滑块
    const slider = document.querySelector('.featured-slider');
    if (slider) {
        initSlider(slider);
    }

    // 消息提示关闭
    const messages = document.querySelectorAll('.message');
    messages.forEach(function(message) {
        const closeBtn = message.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => message.remove(), 300);
            });
        }
    });

    // 评论回复
    const replyButtons = document.querySelectorAll('.comment-actions .reply-btn');
    replyButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const commentId = this.dataset.commentId;
            const replyForm = document.getElementById('reply-form-' + commentId);
            if (replyForm) {
                replyForm.style.display = 'block';
                replyForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });

    // 取消回复
    const cancelReplyButtons = document.querySelectorAll('.cancel-reply');
    cancelReplyButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const form = this.closest('.reply-form');
            if (form) {
                form.style.display = 'none';
            }
        });
    });

    // 代码块复制按钮
    const codeBlocks = document.querySelectorAll('.post-content pre');
    codeBlocks.forEach(function(block) {
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';
        block.parentNode.insertBefore(wrapper, block);
        wrapper.appendChild(block);

        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-code-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i> 复制';
        copyBtn.addEventListener('click', function() {
            const code = block.querySelector('code');
            if (code) {
                navigator.clipboard.writeText(code.textContent).then(function() {
                    copyBtn.innerHTML = '<i class="fas fa-check"></i> 已复制';
                    setTimeout(function() {
                        copyBtn.innerHTML = '<i class="fas fa-copy"></i> 复制';
                    }, 2000);
                });
            }
        });
        wrapper.style.position = 'relative';
        copyBtn.style.position = 'absolute';
        copyBtn.style.top = '0.5rem';
        copyBtn.style.right = '0.5rem';
        wrapper.appendChild(copyBtn);
    });

    // 图片灯箱
    const galleryImages = document.querySelectorAll('.gallery-item img, .post-content img');
    galleryImages.forEach(function(img) {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            openLightbox(this.src);
        });
    });

    // 脚注交互
    const footnotes = document.querySelectorAll('.footnote');
    footnotes.forEach(function(footnote) {
        footnote.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // 懒加载图片
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(function(img) {
            imageObserver.observe(img);
        });
    }

    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    // 搜索表单
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const query = this.querySelector('input[name="q"]').value.trim();
            if (!query) {
                e.preventDefault();
                alert('请输入搜索关键词');
            }
        });
    }

    // 归档年份折叠
    const archiveYears = document.querySelectorAll('.archive-year');
    archiveYears.forEach(function(year) {
        const title = year.querySelector('.archive-year-title');
        if (title) {
            title.style.cursor = 'pointer';
            title.addEventListener('click', function() {
                const posts = year.querySelector('.archive-posts');
                if (posts) {
                    posts.style.display = posts.style.display === 'none' ? 'block' : 'none';
                }
            });
        }
    });

    // 返回顶部
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.className = 'scroll-top-btn';
    scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollTopBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #C5A059;
        color: white;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        z-index: 9999;
        display: none;
        transition: all 0.3s ease;
    `;
    document.body.appendChild(scrollTopBtn);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTopBtn.style.display = 'flex';
            scrollTopBtn.style.alignItems = 'center';
            scrollTopBtn.style.justifyContent = 'center';
        } else {
            scrollTopBtn.style.display = 'none';
        }
    });

    scrollTopBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // 鼠标悬停效果
    const cards = document.querySelectorAll('.post-card, .archive-post');
    cards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.zIndex = '10';
        });
        card.addEventListener('mouseleave', function() {
            this.style.zIndex = '1';
        });
    });
});

/**
 * 初始化特色文章滑块
 */
function initSlider(slider) {
    const slides = slider.querySelectorAll('.slider-slide');
    const dotsContainer = slider.querySelector('.slider-controls');
    const prevBtn = slider.querySelector('.slider-nav.prev');
    const nextBtn = slider.querySelector('.slider-nav.next');

    if (slides.length <= 1) return;

    let currentSlide = 0;
    let autoplayInterval;

    // 创建导航点
    slides.forEach(function(_, index) {
        const dot = document.createElement('button');
        dot.className = 'slider-dot' + (index === 0 ? ' active' : '');
        dot.addEventListener('click', function() {
            goToSlide(index);
        });
        dotsContainer.appendChild(dot);
    });

    const dots = slider.querySelectorAll('.slider-dot');

    function goToSlide(index) {
        currentSlide = index;
        if (currentSlide >= slides.length) currentSlide = 0;
        if (currentSlide < 0) currentSlide = slides.length - 1;

        const container = slider.querySelector('.slider-container');
        container.style.transform = `translateX(-${currentSlide * 100}%)`;

        dots.forEach(function(dot, i) {
            dot.classList.toggle('active', i === currentSlide);
        });
    }

    function nextSlide() {
        goToSlide(currentSlide + 1);
    }

    function prevSlide() {
        goToSlide(currentSlide - 1);
    }

    // 按钮事件
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);

    // 自动播放
    function startAutoplay() {
        autoplayInterval = setInterval(nextSlide, 5000);
    }

    function stopAutoplay() {
        clearInterval(autoplayInterval);
    }

    // 鼠标悬停暂停
    slider.addEventListener('mouseenter', stopAutoplay);
    slider.addEventListener('mouseleave', startAutoplay);

    startAutoplay();

    // 触摸滑动支持
    let touchStartX = 0;
    let touchEndX = 0;

    slider.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
        stopAutoplay();
    }, { passive: true });

    slider.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
        startAutoplay();
    }, { passive: true });

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                nextSlide();
            } else {
                prevSlide();
            }
        }
    }
}

/**
 * 打开图片灯箱
 */
function openLightbox(src) {
    const lightbox = document.createElement('div');
    lightbox.id = 'lightbox';
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    `;

    const img = document.createElement('img');
    img.src = src;
    img.style.maxWidth = '90%';
    img.style.maxHeight = '90%';
    img.style.borderRadius = '8px';

    lightbox.appendChild(img);
    document.body.appendChild(lightbox);

    lightbox.addEventListener('click', function() {
        lightbox.remove();
    });

    // ESC关闭
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            lightbox.remove();
        }
    });
}

/**
 * 显示消息提示
 */
function showMessage(message, type = 'info') {
    const container = document.querySelector('.messages') || createMessagesContainer();
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    msg.innerHTML = `
        ${message}
        <button class="close-btn">&times;</button>
    `;

    container.appendChild(msg);

    const closeBtn = msg.querySelector('.close-btn');
    closeBtn.addEventListener('click', function() {
        msg.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => msg.remove(), 300);
    });

    setTimeout(function() {
        msg.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => msg.remove(), 300);
    }, 5000);
}

function createMessagesContainer() {
    const container = document.createElement('div');
    container.className = 'messages';
    document.body.appendChild(container);
    return container;
}

// 添加slideOut动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
