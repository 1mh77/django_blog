# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'userprofile'

# django 会根据用户请求的URL来决定使用那个视图
# 例如当用户请求 userprofile/login 时，会调用 views 里面的 user_login 函数，返回渲染后的对象。

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('delete/<int:id>/', views.user_delete, name='delete'),
    path('edit/<int:id>/', views.profile_edit, name='edit'),
]