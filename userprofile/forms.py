# -*- coding: utf-8 -*-
'''
@Time    : 2022/5/12 8:17
@Author  : 李铭晖
@File    : form.py
'''


from .models import Profile

from django import forms
from django.contrib.auth.models import User

# 登陆表单，继承了forms.Form类
# 前面写文章模块继承的是forms.ModelForm类，这个类适合需要直接与数据库交互的功能
# 写文章需要和数据库交互
# 用户登录不需要数据库进行改动，因此继承forms.Form就可以
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserRegisterForm(forms.ModelForm):
    # 复写user的密码
    password = forms.CharField()
    password2 = forms.CharField()

    # class meta不加括号
    class Meta:
        model = User
        # 查了百度给的报错：类需要更新
        # 才发现这里变量名带了个s
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    # def clean_[字段]这种写法会自动调用django，对单个字段的数据进行清洗
    def clean_password2(self):
        # 注意这里要写password2的方法，如果用password方法会导致password2被清洗掉，导致两次密码输入不一致
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            return forms.ValidationError('密码输入不一致，请重试')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')