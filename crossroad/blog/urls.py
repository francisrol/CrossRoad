from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    # 默认首页
	url(r'^$', views.IndexView.as_view(), name='index'),
	# 对应分类首页
	url(r'^category/(?P<category>\w+)/$', views.IndexView.as_view(), name='category'),
	# 标签列表页
	url(r'^tags/(?P<tags>.+)/$', views.IndexView.as_view(), name='tags'),
	# 文章内容详情
	url(r'^blog/(?P<alias>[\w-]+)/(?P<slug>[\w]+)/$', views.BlogDetailView.as_view(), {'order_by':'pub_date'}, name='blog_detail'),
]