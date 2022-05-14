# -*- coding: utf-8 -*-
'''
@Time    : 2022/5/13 10:12
@Author  : 李铭晖
@File    : urls.py
'''

from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
]
