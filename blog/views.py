from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from utils import custom_paginator
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q

from .models import Post, Category, Tag
# Create your views here.


def index(request):
    post_list = Post.objects.all().order_by('-created_time')

    return render(request, 'index.html', locals())


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'post_list'
    # 开启分页功能，每页放2条数据
    paginate_by = 2

    # 重写get_context_data,一遍放入我们的分页的起始页面和结束页码
    def get_context_data(self, **kwargs):
        # 调用父类的get_context_data方法
        context = super().get_context_data(**kwargs)
        # 获取分页相关的变量
        page = context.get('page_obj')
        paginator = context.get('paginator')

        # 调用我们自定义的分页方法。
        start, end = custom_paginator(page.number, paginator.num_pages, 4)
        # 将我们的start和end写入context中
        context.update({
            'page_range': range(start, end+1)
        })
        # 返回context
        return context




def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 生成评论form表单
    form = CommentForm()
    # 把post的评论列表传到前台
    comment_list = post.comment_set.all().order_by('-created_time')
    post.content = markdown.markdown(post.content,
                        extensions=[
                            'markdown.extensions.extra',
                            'markdown.extensions.codehilite',
                            'markdown.extensions.toc'
                        ])
    post.increase_views()
    return render(request, 'blog/detail.html', locals())


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    # 重写get方法，以便我们可以执行我们自己定义的increase_views方法
    def get(self, *args, **kwargs):
        # 调用父类的get方法。以便self.object中有我们需要的post实例对象
        response = super().get(*args, **kwargs)
        # 调用我们自己定义的increase_views方法
        self.object.increase_views()
        # print(kwargs.get('pk'))
        # 返回response对象
        return response

    # 重写get_object方法，以便支持markdown语法
    def get_object(self, queryset=None):
        # 调用父类的get_object方法。
        post = super().get_object()

        # 对post的content进行markdown处理。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        post.content = md.convert(post.content)
        # 讲markdown的目录赋值给post
        post.toc = md.toc
        return post

    # 重写get_context_data方法，以便往context中写入额外的变量
    def get_context_data(self, **kwargs):
        # 调用父类的get_context_data，获取已有context对象
        context = super().get_context_data(**kwargs)
        # 生成前台需要使用的评论表单
        form = CommentForm()
        # 获取post实例
        post = context['post']
        # 查出post对应的评论列表
        comment_list = post.comment_set.all().order_by('-created_time')
        # 使用字典的update方法，来更新context字典。
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        # 最后返回更新后的context
        return context





def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by("-created_time")
    return render(request, 'index.html', locals())


class ArchivesView(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                    created_time__month=self.kwargs.get('month')).order_by('-created_time')

def categories(request, pk):
    # 根据pk取得category对象
    category = get_object_or_404(Category, pk=pk)
    # 根据取得category来正向查找post
    # post_list = Post.objects.filter(category=category)
    # 反向查
    post_list = category.post_set.all()
    return render(request, 'index.html', {'post_list': post_list})


class CategoriesView(IndexView):
    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=category)


class TagsView(IndexView):
    # 重写get_queryset方法，修改默认的查询行为。
    def get_queryset(self):
        # 先根据pk查出tag对象
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        # 有了tag对象之后，根据这个tag对象，查出tag下的post文章。
        return super().get_queryset().filter(tag=tag)


def search(request):
    # 获取q变量
    q = request.GET.get('q')
    # 定义一个错误提示变量
    error_msg = ""
    # 判断q是否存在，即用户是否输入搜索关键词。
    if not q:
        # 如果不存在，则提示用户输入搜索关键词
        error_msg = '请输入搜索关键词'
        # 返回首页
        return render(request, 'index.html', {'error_msg': error_msg})
    # 如果用户提交了搜索关键词。那么使用搜索关键词进行查找
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    # 返回结果
    return render(request, 'index.html', {'post_list': post_list})
