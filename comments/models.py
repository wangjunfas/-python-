from django.db import models

# Create your models here.


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    url = models.URLField()
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    # 定义外键关系
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]