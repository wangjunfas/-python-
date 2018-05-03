from django.db import models
from users.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    # 摘要
    excerpt = models.CharField(max_length=200, blank=True, null=True, verbose_name='简介')

    # 创建时间和更新时间。
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    # 定义关联关系
    category = models.ForeignKey('Category', verbose_name='类别')
    tag = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    author = models.ForeignKey(User, verbose_name='作者')
    # 增加文章阅读数，默认是0
    views = models.PositiveIntegerField(default=0)

    # 重写save方法，实现自动生成摘要
    def save(self, *args, **kwargs):
        # 如果没有指定摘要。则自动生成
        if not self.excerpt:
            # 首先生成markdown的对象实例。
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ])
            # 使用markdown的convert函数，转化self.content。然后去掉html标签，再然后取前54个字符
            self.excerpt = strip_tags(md.convert(self.content))[:54]
        # 最后调用父类的save方法。
        super().save(*args, **kwargs)

    # 增加计算文章阅读数的方法
    def increase_views(self):
        # 每次调用此方法，就把views加1
        self.views += 1
        # 只更新views字段
        self.save(update_fields=['views'])


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # /post/1/
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = '帖子'
        verbose_name = '帖子'
        ordering = ['-created_time']
