from django.views import generic

from .models import Blog
from .filters import search,blog_filter


class IndexView(generic.ListView):
    model = Blog                          #显示内容的模板类
    template_name = 'blog/index.html'    #前端html模板
    paginate_by = 5                        #每页条目数
    paginate_orphans = 1                #最大孤页显示条目数

    #以下为非继承的类属性
    #设置全文检索的查找范围
    search_fields = ['title','summary']
    searched = False    #判断是否经过查询
    btype_num_list = None    #对筛选结果计数后组成的一个，BlogType分类的list，作为上下文发送给前端
    btype_uri = ''    #将进行分类查询的字符串，作为上下文发送给前端，以便前端组成url

    # 处理queryset对象
    def get_queryset(self):
        category = self.kwargs.get('category')
        tags = self.kwargs.get('tags')
        querysets = None
        # 判断url是否来自category
        if category:
            querysets = Blog.objects.filter(blogcategory__alias=category)
        elif tags:
            querysets = Blog.objects.filter(blogtag__alias=tags)
        else:
            querysets = Blog.objects.all()

        # 处理搜索框的搜索字符串， 返回查询的结果，没有则返回原始传入的数据querysets
        query_results, self.searched = search(self.request, querysets, self.search_fields)

        # 获取标签筛选的字符串，没有则为‘’
        tags_string = self.request.GET.get('tag') or ''
        tags_list = set(tags_string.split(','))
        self.btags_uri = ','.join(tags_list)    #赋给类属性

        # 对query_results进行标签类型的筛选
        queryset_list, self.btags_num_list = blog_filter(query_results, tags_list)
        return queryset_list.order_by('-pub_date')

    # 处理返回的上下文
    def get_context_data(self, **kwargs):
        #获取为处理过的上下文数据
        context = super(IndexView,self).get_context_data(**kwargs)

        #以下均为新增的上下文，以便在前端进行布局，设置超链接url等
        if self.searched:
            results_num = context['paginator'].count
            # 文章数量
            context['results_num'] = results_num
            # 查询字符串
            context['form_string'] = self.request.GET.get('q','')
        # 标签列表数据
        context['btags_num_list'] = self.btags_num_list
        # 本次请求标签的内容
        context['btags_uri'] = self.btags_uri
        context['abs_url'] = self.request.get_raw_uri().split('?')[0]
        return context

# 文章内容视图
class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    search_fields = ['title','content']
    searched = False

    #重写父类get_context_data方法
    def get_context_data(self,**kwargs):
        #获取为处理过的上下文数据
        order_by = self.kwargs.get('order_by')
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        #以下均为新增的上下文，以便在前端进行布局，设置超链接url等
        alias = self.kwargs.get('alias')
        query_results,self.searched = search(self.request,Blog.objects.filter(blogcategory__alias=alias), \
                                             self.search_fields)
        querysets = query_results.order_by(order_by)
        if self.searched:
            results_num = querysets.count()
            context['results_num'] = results_num
            context['form_string'] = self.request.GET.get('q','')
        context['object_list'] = querysets
        context['abs_url'] = self.request.get_raw_uri().split('?')[0]
        return context


