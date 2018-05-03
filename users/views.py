from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .forms import RegisterForm, EditForm
from .models import User
# Create your views here.


def register(request):
    # 获取next即跳转地址
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    # 首先判断request.method是否是post方法
    if request.method == 'POST':
        # 使用request中的数据，初始化form表单
        form = RegisterForm(request.POST, request.FILES)
        # 判断form表单中的数据是否合法
        if form.is_valid():
            # 如果合法，则保存
            form.save()
            messages.success(request, '注册成功，请登录！')
            # 处理跳转
            if redirect_to:
                # 跳转到redirect_to所指定的页面。即注册之前访问的页面
                return redirect(redirect_to)
            else:
                # 跳转到首页
                return redirect(reverse('login'))
    else:
        # 如果不是post方法，即是get,返回注册页面
        # 创建一个form实例对象
        form = RegisterForm()
        # 渲染注册页面
        return render(request, 'users/register.html', {'form': form, 'next':redirect_to})


