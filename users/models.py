from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# 拓展默认的User模型
class User(AbstractUser):
    nickname = models.CharField(max_length=30, verbose_name='昵称')
    headshot = models.ImageField(upload_to='avatar/%Y/%m/%d', default='default.jpg', verbose_name='头像')
    signature = models.CharField(max_length=120, verbose_name='个性签名', default='this guy is too lazy to leave anything here.')

    class Meta(AbstractUser.Meta):
        pass





