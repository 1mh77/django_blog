from django.shortcuts import render

# Create your views here.

# 导入HttpRseponse模块
from .models import ArticlePost
from django.contrib.auth.decorators import login_required


# 引入分页模块
from django.core.paginator import Paginator
# 引入 Q 对象
from django.db.models import Q

def article_list(request):

    '''
    # 根据GET请求查询条件
    # 返回不同排序的对象数组
    if request.GET.get('order') == 'total_views':
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = ArticlePost.objects.all()
        order = 'normal'


    # 修改变量名称（articles -> article_list）
    # article_list = ArticlePost.objects.all()
    '''

    search = request.GET.get('search')
    order = request.GET.get('order')
    # 用户搜索逻辑
    if search:
        if order == 'total_views':
            # 用 Q 对象进行联合搜索
            # Q(title__icontains=search意思是在模型的title字段搜索，多个Q对象用管道符隔开
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()



    # 每页显示 3 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 文章需要翻页，把order 传给模板，告诉模板下一页如何排序
    # 增加search 到context
    context = { 'articles': articles, 'order': order, 'search': search }
    return render(request, 'article/list.html', context)


'''
# 视图函数
def article_list(request):
    # 取出所有博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板的对象
    context = {'articles':articles}
    # render函数：载入模板，并返回contxet对象
    return render(request, 'article/list.html', context)
'''
'''
# 注释里面保存代码的往期版本

def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 需要传递给模板得对象
    context = { 'article':article}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)
'''
# 别忘了导入markdown模块
import markdown
from comment.models import Comment

def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)

    # 取出相应的评论
    comments = Comment.objects.filter(article=id)

    # 浏览量 +1
    article.total_views += 1
    # update_fields 指定只更新total_views字段，优化执行效率
    article.save(update_fields=['total_views'])

    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',

            # 目录扩展
            # 'markdown.extensions.toc'
            # 不要忘记最后的逗号
            'markdown.extensions.toc',
        ])
    # 需要传递给模板de对象
    # 也就是需要模板渲染的内容
    # markdown.toc 哪里就是忘记传入这个了
    context = {'article': article, 'comments':comments}
    # render 函数结合模板和上下文（context),返回渲染后的HttpRsepone对象
    return render(request, 'article/detail.html', context)


'''
import markdown

def article_detail(request, id):
    artile = ArticlePost.objcts.get(id=id)

    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite'
                                     ])
    context = { 'article': article}
    return render(request, 'article/detail.html', context)
'''

# 引入redire重定向模块
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User


# 写文章的视图
@login_required(login_url='userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型要求
        if article_post_form.is_valid():
            # 保存数据，但是暂时不提交到数据库中，因为还没指定作者
            # 我一开始在这里没写commit=False，网页能正常打开，但是提交就会报错
            new_article = article_post_form.save(commit=False)
            # 指定数据库中的id=1为作者

            # 在后期这里改为指定登录的用户位作者，而不是指定的第一个用户
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()
            #完成后返回到文章列表
            return redirect('article:article_list')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse('表单内容有误，请重新填写')
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = { 'article_post_form': article_post_form }
        # 返回模板
        return render(request, 'article/create.html', context)

# 删除文章
def article_delete(request, id):
    # 根据 id 获取要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用delete方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect('article:article_list')

@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse('你没有权限删除这篇文章')
        else:
            article.delete()
            return redirect('article:article_list')
    else:
        return HttpResponse('仅允许post请求')

# 后端鉴权，防止恶意用户直接通过url修改（模板中的鉴权只能拦截好用户）
# @login_required(login_url='/userprofile/login/')
def article_update(request, id):
    '''
    通过POST方法提交表单，更新title，body字段
    get的方法进入出师表单页面

    装饰器过滤未登录用户
    if过滤已登录但不是作者的用户
    '''

    # 获取需要修改的文章对象i
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        # data= 来赋值
        article_post_form = ArticlePostForm(data=request.POST)

        # 先鉴定身份是否位作者用户
        if request.user != article.author:
            return HttpResponse('抱歉，你无权修改这篇文章')
        # 判断提交的数据是否满足模型的要求
        # 一开始把valid写成了vaild,导致报错，说找不到url
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            # 完成后返回修改后的文章页面，需要传入文章的id
            # 写完了这里结果没写保存
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse('表单内容有误，请重新提交')
    # 如果用户 GET 请求数据
    else:
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象传递进去，以便提取旧的内同
        context = { 'article':article, 'article_post_form': article_post_form }
        # 将响应返回模板中
        return render(request, 'article/update.html', context)