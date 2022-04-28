from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Blog
from . forms import CommentForm
# Create your views here.
#blog_pk是URL实名参数
def blog_comment(request,blog_pk):
    blog = get_object_or_404(Blog,pk=blog_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            #commit = False的作用是生成Comment类的实例对象，但不立刻保存到数据库表中
            comment = form.save(commit=False)
            #用户登录后，request.user保存用户的nikename、email等值
            comment.name = request.user.nikename
            comment.email = request.user.email
            #通过外键关系将评论和被评论的文章关联起来
            comment.blog = blog
            #真正的保存到数据库
            comment.save()
            return redirect(blog)
        else:
            #数据渲染不通过，需要重新渲染页面，需要传递三个模板变量给detail.html，文章（blog），评论列表、表单对象（form）
            comment_list =blog.comment_set.all()
            context = {
                'blog':blog,
                'form':form,
                'comment_list':comment_list,
            }
            return render(request,'blog/detail.html',context=context)
    #如果请求方式不是POST，说明第一次打开网页，重定向到实例对象blog的get_absolute_url()方法返回的地址
    return redirect(blog)
