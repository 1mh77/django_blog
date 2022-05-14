# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/25 21:23
@Author  : 李铭晖
@File    : urls.py
'''

# 引入views（漏了这个结果在runsever里面报错了，说找不到views
# 点(.)代表从相对导入，相对导入的意思是从当前项目中寻找需要导入的包或者函数
from . import views

from django.urls import path

app_name = 'article'

urlpatterns = [
    # path函数将url映射到视图
    # 他妈的加完一个path不加逗号，前面几个居然都没出错，一直没发现
    path('article-list/',views.article_list, name='article_list'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article-create/', views.article_create, name='article_create'),
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    path(
        'artile-safe-delete/<int:id>/',
        views.article_safe_delete,
        name='article_safe_delete',
    ),
    path('article-update/<int:id>/', views.article_update, name='article_update'),
]