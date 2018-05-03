from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post
from .forms import CommentForm
# Create your views here.


def post_comment(request, pk):
    # 根据提交的comment数据创建一个comment对象。并保存
    # 然后把这个对象的post属性设置好。即这个comment属于哪个post

    # 首先根据传入的pk获取post对象
    post = get_object_or_404(Post, pk=pk)

    # 判断提交方法是否是post
    if request.method == 'POST':
        # 使用request.POST中的数据，生成commentform的实例
        form = CommentForm(request.POST)
        # 判断form中的数据是否合法。
        if form.is_valid():
            # 先通过save创建一个实例，不保存到数据库中。
            comment = form.save(commit=False)
            # 将post对象写入comment对象中
            comment.post = post
            # 一切数据ok，可以写入数据库中
            comment.save()
        else:
            # 如果数据不合法，则返回原界面。
            # 需要传form对象，post，post的评论列表

            # 取出post的评论列表，通过post来反向取
            comment_list = post.comment_set.all().order_by('-created_time')
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context)
    return redirect(post)


