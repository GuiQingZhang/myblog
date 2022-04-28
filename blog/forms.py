#导入forms类
from django import forms
#导入该应用程序的数据模型
from . import models
#导入出错信息处理模块
from django.core.exceptions import ValidationError
#定义一个继承Form类的reg_form,这也是一个类
class reg_form(forms.Form):
    username = forms.CharField(
        max_length = 20,
        label = '登录账号',
        error_messages={
            'max_length':'登录账号不能超过20位',
            'required':'登录账号不能为空',
        },
        widget = forms.widgets.TextInput(attrs={'class':'form-control'},)
    )
    password = forms.CharField(
        min_length = 6,
        label = '密码',
        error_messages={
            'min_length':'密码最少六位',
            'required':'密码不能为空',
        },
        widget = forms.widgets.PasswordInput(attrs={'class':'form-control'},render_value=True)
    )
    #增加一个repassword字段，让用户输入密码时进行两次输入，保证注册密码正确
    repassword = forms.CharField(
         min_length = 6,
        label = '密码',
        error_messages={
            'min_length':'密码最少六位',
            'required':'密码不能为空',
        },
        widget = forms.widgets.PasswordInput(attrs={'class':'form-control'},render_value=True)
    )
    nikename = forms.CharField(
        max_length = 20,
        required = False,
        label = '昵称',
        error_messages={
            'max_length':'姓名长度不能超过20位',
        },
        #如果不输入nikename字段值，默认值为'博客用户'
        initial='博客用户',
        widget = forms.widgets.TextInput(attrs={'class':'form-control'})
    )
    email = forms.EmailField(
        label='邮箱',
        error_messages={
            'invalid':'请输入正确格式的邮箱',
            'required':'邮箱不能为空',
        },
        widget = forms.widgets.EmailInput(attrs={'class':'form-control'})
    )
    telephone = forms.CharField(
        max_length = 11,
        label = '电话号码',
        required = False,
        error_messages={
            'max_length':'最长长度不能超过11位',
        },
        widget = forms.widgets.TextInput(attrs={'class':'form-control'})
    )
    #head_img位ImageField类型，在页面生成<input type='file'>标签
    head_img = forms.ImageField(
        label = '头像',
        #在attrs中设置style为display:none是为了在页面中不显示这个标签
        widget = forms.widgets.FileInput(attrs={'style':'display:none'})
    )
    #定义一个校验字段的函数，校验字段函数命名是有规则的，形如：clean_字段名(),这个函数保证username值不重复
    def clean_username(self):
        uname = self.cleaned_data.get('username')
        #从数据库中查询是否有同名的记录
        vexist = models.loguser.objects.filter(username=uname)
        if vexist:
            self.add_error('username',ValidationError('登录账号已存在！'))
        else:
            return uname
    #定义一个校验程序，判断两次输入的密码是否一致
    def clean_repassword(self):
        passwd = self.cleaned_data.get('password')
        repasswd = self.cleaned_data.get('repassword')
        if repasswd != passwd:
            self.add_error('repassword',ValidationError('两次输入的密码不一致！'))
        else:
            return repasswd
    