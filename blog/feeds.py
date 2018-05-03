from django.contrib.syndication.views import Feed

from .models import Post


# 编写自定义的Feed类
class AllPostFeed(Feed):
    # 配置显示在聚合阅读器上的标题
    title = '千峰博客'

    # 配置通过聚合阅读器访问我们博客的url地址
    link = '/index/'

    # 配置显示在聚合阅读器上的描述信息
    description = '千峰博客订阅测试'

    # 配置显示在聚合阅读器上的条目
    def items(self):
        return Post.objects.all()

    # 配置聚合阅读器上条目的显示标题
    def item_title(self, item):
        return '[%s]%s' % (item.category, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.content


