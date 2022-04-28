#导入haystack中的相关模块indexes
from haystack import indexes
from .models import Blog

#建立索引类名，名字规定为：'modelnameIndex'，类必须继承index.SearchIndex、indexes.Indexable
class BlogIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)
    #重写get_model()方法，放回相应的数据模型，这个方法必须有
    def get_model(self):
        return Blog
    #重写index_queryset()方法，返回数据模型需要检索的记录
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
