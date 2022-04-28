#导入static模块为静态文件服务，静态文件主要包括图片文件、JavaScript文件、css文件
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',include('blog.urls')),
    path('comments/',include('comments.urls')),
    #通过include('ckeditor_upload.urls')导入富文本编辑器ckeditor封装好的URL配置
    path('ckeditor/',include('ckeditor_uploader.urls')),
     path('search/',include('haystack.urls')),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
