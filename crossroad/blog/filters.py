import operator
from functools import reduce

from django.db.models import Q

from .models import BlogType

#全文搜索
#进行字词查询，Queryset Object，搜索范围，查询字符串
def get_search_results(queryset,search_field,search_term):
	def construct_search(field_name):
		#设置搜索起始分类，均无视大小写，分别是，，
		if field_name.startswith('^'):  #开头匹配
			return "%s__istartswith" % field_name[1:]
		elif field_name.startswith('='):  #全部匹配，
			return "%s__iexact" % field_name[1:]
		else:
			return "%s__icontains" % field_name  #全文部分匹配

	if search_field and search_field:
		orm_lookups = [construct_search(str(f_name)) for f_name in search_field]	
		for word in search_term.split():	#将查询字符串分词，暂时只支持查询时手动用空格进行非此查询，此时一个无空格句子会被看为一个词语
			orm_queries = [Q(**{orm_lookup:word}) for orm_lookup in orm_lookups]	#Q函数可对Queryset对象进行‘与或非’的筛选
			queryset = queryset.filter(reduce(operator.or_,orm_queries))
	return queryset

def search(request,queryset,fields):
	query_string = request.GET.get('q','')
	#检验用户是否输入数据进行搜索
	searched = False
	if query_string:
		searched = True
	results = get_search_results(queryset,fields,query_string)
	return results,searched

#进行分类筛选，参数分别是一个Queryset Object，和一个分类查询的字符串
#返回一个筛选后的Queryset Object，和一个包含了各个分类所包含的文章数目的list，供前端使用
def blog_filter(queryset_list,alias_string):
	alias_list = alias_string.split()
	bt_list = []
	BT = BlogType.objects.all()
	for al in alias_list:
		if BT.filter(alias=al).exists:
			queryset_list = queryset_list.filter(blogtype__alias=al)
	aliases = BT.values_list('alias','btype')
	for bt in aliases:
		num = queryset_list.filter(blogtype__alias=bt[0]).count()
		if num:
			bt_list.append((bt[1],bt[0],num))
	return queryset_list,bt_list

'''
#之前尝试分类查询的方法，已被blog_filter改进，替换
def get_btype_num(queryset_list):
	py=0
	yc=0
	zz=0
	yj=0
	for blog in queryset_list:
		for bt in blog.blogtype.all():
			if bt.btype == 'python':
				py = py + 1
			if bt.btype == '原创':
				yc = yc + 1
			if bt.btype == '转载':
				zz = zz + 1
			if bt.btype == '原创教程':
				yj = yj + 1
	return [('python','py',py),('原创','yc',yc),('转载','zz',zz),('原创教程','yj',yj)]
def get_btype_blog_list(queryset_list,btype_string):
	btype_list = btype_string.split()
	for btype in btype_list:
		if btype and btype in ['py','yc','zz','yj']:
			btype_id = {'py':3,'yc':2,'zz':1,'yj':5}.get(btype)
			queryset_list = queryset_list.filter(blogtype__pk=btype_id)
	return queryset_list
'''