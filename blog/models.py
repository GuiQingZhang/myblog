from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
#调用富文本编辑相关模块，从富文本编辑器ckeditor_uploader.fields中导入RichTextUploadingField
from ckeditor_uploader.fields import RichTextUploadingField
#导入strip_tags()函数，代码中用这个函数截取字段中的字符串
from django.utils.html import strip_tags
# Create your models here.

#Django用户认证系统提供了一个内置的User对象，我们想通过扩展这个用户以增加新字段，扩展方式可以通过继承AbstractUser的方式，所以要导入AbstractUser类
#建立一个数据模型loguser，继承AbstractUser，就可以生成系统用户
class loguser(AbstractUser):
    #增加一个nikename字段用来存储用户的名字，我们博客相关网站上显示这个名字
    nikename = models.CharField(max_length=32,verbose_name='昵称',blank=True)
    telephone =models.CharField(max_length=11,null=True,unique=True)
    head_img = models.ImageField(upload_to='headimage',blank=True,null=True,verbose_name='头像')
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name
        
class Category(models.Model):
    name = models.CharField(max_length=32,verbose_name='分类名')
    des = models.CharField(max_length=100,verbose_name='备注',null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

class Tag(models.Model):
    name = models.CharField(max_length=32,verbose_name='标签名')
    des = models.CharField(max_length=100,verbose_name='备注')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

class Blog(models.Model):
    title = models.CharField(max_length=70,verbose_name='文字标题')
    #文字正文使用富文本编辑器进行博客文章排版
    #body = RichTextUploadingField(config_name='test',verbose_name='文本内容')
    body = RichTextUploadingField(verbose_name='文本内容')
    #文章的创建时间，存储时间用DateTimeField类型
    created_time = models.DateTimeField(verbose_name='创建时间')
    modified_time = models.DateTimeField(verbose_name='修改时间')
    #excerpt字段存储文章摘要，指定blank=True就可以允许为空值了
    excerpt = models.CharField(max_length=200,blank=True,verbose_name='文章摘要')
    #categroy是设置文章分类字段，与前面的Categroy是多对一关系
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='分类')
    #tags为文章标签，多对多关系，设置blank=True以允许文章没有标签
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签')
    #author为文章作者，我们用loguser表中定义的用户，这里用外键与该表关联
    author = models.ForeignKey(loguser,on_delete=models.CASCADE,verbose_name='作者')
    #记录文章阅读量，起始值为0，为该字段定义一个increase_view()函数
    views = models.IntegerField(default=0,verbose_name='查看次数')
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
    #increase_view()把views字段的值加1然后保存到数据
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    #save()函数是数据模型类的方法，我们重写这个方法是为了自动提取摘要内容
    def save(self,*args,**kwargs):
        if not self.excerpt:
            #由于文章是用富文本编辑器写的，文中带有大量HTML标签，使用strip()函数可能会把HTML标签截断，所以这里使用strip_tags()把字段中的HTML标签山区，然后在纯文本中截取字符串
            self.excerpt = strip_tags(self.body)[:118]
            #调用父类的save()方法将数据保存到数据库中
            super(Blog,self).save(*args,**kwargs)
        else:
            super(Blog,self).save(*args,**kwargs)
    def __str__(self):
        return self.title
    class Meta:
        #设置created_time的值倒序排列，这样最新的文章排在前面
        ordering = ['-created_time']
        verbose_name = '文档管理表'
        verbose_name_plural = '文档管理表'

