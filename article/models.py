# Create your models here.
from django.urls import reverse
from django.db import models
# 导入内建的User模型
from django.contrib.auth.models import User
# timezone处理事件相关的事务
from django.utils import timezone


# 博客文章数据类型
class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。model.CharField 为字符串字段，用于保存比较短的字符串，比如标题。这个属性是其他类的实例
    title = models.CharField(max_length=100)

    # 文章正文，保存大量文本用TextField
    body = models.TextField()

    #文章创建时间。参数default=timezone.now 指定其在创建数据时将默认写入当前
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 存储浏览量
    total_views = models.PositiveIntegerField(default=0)

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])


    #meta 是“元”的意思，元数据的元
    # 元数据指的是任何不是字段的东西，这些东西是整个表的共同行为，像是排序、数据库表名等等
    class Meta():
        # ordering指定模型返回的数据的排列顺序
        # '-created'表明数据应该以倒序排列
        ordering = ('-created',)


    # 函数__str__定义当吊桶对象的 str() 方法是的返回值的内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title
