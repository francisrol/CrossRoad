import operator
from functools import reduce

from django.db.models import Q

from .models import BlogTags

#全文搜索
#进行字词查询，Queryset Object，搜索范围，查询字符串
def get_search_results(queryset, search_fields, query_string):
    def construct_search(field_name):
        #设置搜索起始分类，均无视大小写，分别是，，
        if field_name.startswith('^'):  #开头匹配
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):  #完全匹配，
            return "%s__iexact" % field_name[1:]
        else:
            return "%s__icontains" % field_name  #全文部分匹配

    if search_fields and query_string:
        # 结构化查询方式：从头匹配、完全匹配、全文部分匹配
        orm_lookups = [construct_search(str(f_name)) for f_name in search_fields]
        # 查询字符串分词，暂时只支持查询时手动用空格进行非此查询，此时一个无空格句子会被看为一个词语
        for word in query_string.split():
            # Q函数返回的对象可以对Queryset对象进行‘与或’运算
            orm_queries = [Q(**{orm_lookup: word}) for orm_lookup in orm_lookups]
            # operator.or_ 对各个Q函数对象两两进行或运算
            queryset = queryset.filter(reduce(operator.or_, orm_queries))
    return queryset

def search(request, queryset, search_fields):
    query_string = request.GET.get('q')
    #检验用户是否输入数据进行搜索
    searched = False
    # 如果有查询字符串，则改为True
    if query_string:
        searched = True
    results = get_search_results(queryset, search_fields, query_string)
    return results, searched

# 标签筛选，参数分别是一个Queryset Object，和一个由各个标签组成的字符串
# 返回一个筛选后的Queryset Object，和一个包含了各个分类所包含的文章数目的list，供前端使用
def blog_filter(blog_queryset_list, tags_list):
    tag_queryset_list = []
    blogtags_querysets = BlogTags.objects.all()
    # 对tag列表对应的文章进行过滤筛选
    for tag in tags_list:
        if tag:
            if blogtags_querysets.filter(alias=tag.strip()).exists:
                blog_queryset_list = blog_queryset_list.filter(blogtag__alias=tag)
    # 获取所有的标签类型
    tags_querysets = blogtags_querysets.values_list('alias', 'btag')
    for tag_queryset in tags_querysets:
        # 计算过滤后的文章中各种标签包含的文章的数量
        num = blog_queryset_list.filter(blogtag__alias=tag_queryset[0]).count()
        if num:
            tag_queryset_list.append((tag_queryset[1], tag_queryset[0], num))
    # 返回过滤后的文章数据，和各个标签所含文章书据的列表
    return blog_queryset_list, tag_queryset_list

