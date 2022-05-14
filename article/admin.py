from django.contrib import admin

# Register your models here.

#导入ArticlePost
from .models import ArticlePost

TIME_ZONE = 'Asia/Shanghai'

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)