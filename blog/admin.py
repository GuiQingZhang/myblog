from csv import list_dialects
from django.contrib import admin
from .models import Blog,Category,Tag,loguser
# Register your models here.
#定义一个自定义数据显示管理模型，要继承ModelAdmin类
class BlogAdmin(admin.ModelAdmin):
    #定义管理后台列表页面上显示的字段
    list_display = ('title','created_time','modified_time','category','author','views',)
#注册博客，有第二个参数，按照BlogAdmin定义进行管理
admin.site.register(Blog,BlogAdmin)
#注册loguser、Tag、categroy，没有自定义管理模型类，将按Django admin后台默认页面样式进行管理
admin.site.register(loguser)
admin.site.register(Category)
admin.site.register(Tag)

