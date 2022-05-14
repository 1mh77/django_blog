# -*- coding: utf-8 -*-
'''
@Time    : 2022/5/13 10:11
@Author  : 李铭晖
@File    : forms.py
'''

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']