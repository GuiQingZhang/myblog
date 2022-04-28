from multiprocessing import context
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from . import models
from . import forms
#导入Django认证模块，因为代码中要模拟用户登录
from django.contrib.auth.models import auth
#导入DetaView类
from django.views.generic import DetailView,ListView
from comments.forms import CommentForm
# Create your views here.

def test_ckeditor_front(request):
    #从loguser中取出第一条记录，loguser继承AbstractUser，也就是说loguser中的成员是系统用户，为了测试取出第一条
    user_obj = models.loguser.objects.all().first()
    #通过认证模块让用户处于登录状态
    auth.login(request,user_obj)
    #取出第一条测试数据
    blog = models.Blog.objects.get(id=1)
    #把数据传给页面
    return render(request,'blog/test_ckeditor_front.html',{'blog':blog})

def registe(request):
    if request.method == 'POST':
        form_obj = forms.reg_form(request.POST,request.FILES)
        #判断表单是否通过
        if form_obj.is_valid():
            form_obj.cleaned_data.pop('repassword')
            #由于数据模型继承于AbstractUser类，通过传递**form_obj。cleaned_data和is_staff=1,is_superuser=1设置新生成的用户是系统用户且是超级用户
            user_obj = models.loguser.objects.create_user(**form_obj.cleaned_data,is_staff=1,is_superuser=1)
            auth.login(request,user_obj)
            return redirect('/blog/index')
        else:
            return render(request,'blog/registe.html',{'formobj':form_obj})
    form_obj = forms.reg_form()
    return render(request,'blog/registe.html',{'formobj':form_obj}) 

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #利用auth模块做用户名和密码的校验，如果不通过，user就是none
        user = auth.authenticate(username=username,password=password)
        #校验通过user才有值，user有值说明user对象是系统认证用户
        if user:
            #设置用户为登录状态，并将登录用户对象赋值给request.user，可以在代码和模板文件中直接调用request.name
            auth.login(request,user)
            return redirect('/blog/index')
        else:
            #如果用户为空，说明认证不通过，给出错误信息
            errormsg = '用户名或者密码错误!'
            return render(request,'blog/login.html',{'error':errormsg})
    #在请求方式为GET时，通过render打开页面
    return render(request,'blog/login.html')

def logout(request):
    #调用认证模块，执行logout()函数，这样会把用户相关的cookie、session清空
    auth.logout(request)
    #重定向到首页
    return redirect('/blog/index')

#最新文章
class blogdetailview(DetailView):
    #指定数据模型，从中取出一条记录
    model = models.Blog
    template_name = 'blog/detail.html'
    #指定传给模板文件的模板变量名
    context_object_name = 'blog'
    pa_url_kwarg = 'pk'
    #重写父类get_object()方法，常用于返回定制的数据记录
    def get_object(self,queryset=None):
        blog = super(blogdetailview,self).get_object(queryset=None)
        blog.increase_views()
        return blog
    #
##分类
class categoryview(ListView):
    model = models.Blog
    template_name = 'blog/index.html'
    context_object_name = 'blog_list'
    def get_queryset(self):
        cate = get_object_or_404(models.Category,pk=self.kwargs.get('pk'))
        return super(categoryview,self).get_queryset().filter(category=cate).order_by('-created_time')
#标签
class tagview(ListView):
    model = models.Blog
    template_name = 'blog/index.html'
    context_object_name = 'blog_list'
    def get_queryset(self):
        tag = get_object_or_404(models.Tag,pk=self.kwargs.get('pk'))
        return super(tagview,self).get_queryset().filter(tags=tag).order_by('created_time')
#归档
def archives(request,year,month):
    blog_list = models.Blog.objects.filter(created_time__year=year,created_time__month=month).order_by('-created_time')
    return render(request,'blog/index.html',context={'blog_list':blog_list})

class myindex(ListView):
    model = models.Blog
    template_name = 'blog/index.html'
    context_object_name = 'blog_list'
    def get_queryset(self):
        loguser = get_object_or_404(models.loguser,pk=self.kwargs.get('loguserid'))
        return super(myindex,self).get_queryset().filter(author=loguser).order_by('-created_time')
    #重写父类get_context_data()方法，增加一个模板变量tabname
    def get_context_data(self, **kwargs):
        context = super(myindex,self).get_context_data(**kwargs)
        #在字典中增加一个字典项，键名为'tabname',键值为'mytab'
        context['tabname']='mytab'
        return context

#点击作者头像显示这个作者所有文章
class authorindex(ListView):
    model = models.Blog
    template_name = 'blog/index.html'
    context_object_name = 'blog_list'
    def get_queryset(self):
        #根据URL参数从loguser中选择用户对象
        user = get_object_or_404(models.loguser,pk=self.kwargs.get(id))
        return super(authorindex,self).get_queryset().filter(author=user).order_by('-created_time')
    def get_context_data(self, **kwargs):
        context = super(authorindex,self).get_context_data(**kwargs)
        context['tabname'] = 'firsttab'
        return context

class indexview(ListView):
    model = models.Blog
    template_name = 'blog/index.html'
    context_object_name = 'blog_list'
    #设置每页显示的记录数
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        pageobj = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        #设置每页中分页导航条页面标签的个数
        show_pagenumber = 7
        #调用自定义get_page_data()方法获得显示分页导航条所需要的数据
        page_data = self.get_page_data(is_paginated,paginator,pageobj,show_pagenumber)
        #将page_data更新到context中,page_data是一个字典
        context.update(page_data)
        return context
    #自定义get_page_data()方法，返回当前页的前面页码标签的个数以及后面页码标签的个数
    def get_page_data(self,is_paginated,paginator,pageobj,show_pagenumber):
        #如果没有分页，返回空字典
        if not is_paginated:
            return { }
        left = []
        right = []
        #当前页面数值的获取，得到当前请求的页码号
        cur_page = pageobj.number
        #取出分页中最后的页码
        total = paginator.num_pages
        half = show_pagenumber // 2
        for i in range(cur_page - half,cur_page):
            if i >= 1:
                left.append(i)
        for i in range(cur_page+1,cur_page+half+1):
            if i <= total:
                right.append(i)
        page_date = {
            'left':left,
            'right':right,
        }
        return page_date

class blogdetailview(DetailView):
    model = models.Blog
    template_name = 'blog/detail.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'pk'
    def get_object(self,queryset=None):
        #调用父类get_object()取得一条记录，主键等于URL参数pk的值
        blog = super(blogdetailview,self).get_object(queryset=None)
        #调用这条记录的increase_views方法，把views字段值+1
        blog.increase_views()
        return blog
    def get_context_data(self,**kwargs):
        #调用父类的方法得到一个包含模板变量的字典
        context = super(blogdetailview,self).get_context_data(**kwargs)
        #初始化CommentForm表单
        form = CommentForm()
        #取得本条记录的所有评论
        comment_list = self.object.comment_set.all()
        #在模板变量字典中加入新的字典项
        context.update({
            'form':form,
            'comment_list':comment_list,
        })
        return context