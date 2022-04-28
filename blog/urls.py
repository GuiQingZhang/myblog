from tkinter import N
from django.urls import path,re_path
from . import views
app_name = 'blog'
urlpatterns = [
    path('test_ckeditor_front/',views.test_ckeditor_front),
    #博客首页的URL配置，indexviews继承于通用视图类，不是函数，而URL配置项上只能用函数类型，这里通过as_view()函数告诉Django把这个类当函数用
    path('index/',views.indexview.as_view(),name='index'),
    path('registe/',views.registe,name='registe'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    re_path('blog/(?P<pk>[0-9]+)/',views.blogdetailview.as_view(),name='detail'),
    re_path('category/(?P<pk>[0-9]+)/',views.categoryview.as_view(),name='category'),
    re_path('tag/(?P<pk>[0-9]+)/',views.tagview.as_view(),name='tag'),
    re_path('archives/(?P<year>[0-9]{1,4})/(?P<month>[0-9]{1,2})/',views.archives,name='archives'),
    path('myindex/<int:loguserid>/',views.myindex.as_view(),name='myindex'),
    path('authorindex/<int:id>/',views.authorindex.as_view(),name='authorindex'),
    re_path('blog/(?P<pk>[0-9]+)/',views.blogdetailview.as_view(),name='detail'),
]