import email
from unicodedata import name
from django.db import models

# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=60)
    #评论可能有较长的文本，因此使用TextField类型
    text = models.TextField()
    #created_time字段的auto_now_add = True，这样自动取出本记录保存时间
    created_time = models.DateTimeField(auto_now_add=True)
    #一条评论只能属于一篇文章，但是一篇文章可以有多条评论，文章与评论是一多关系
    blog  = models.ForeignKey('blog.Blog',on_delete=models.CASCADE)
    def __str__(self):
        #取评论前20个字符
        return self.text[:20]