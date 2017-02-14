from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
	url(r'^blog/(?P<alias>[\w-]+)/(?P<pk>[0-9]+)/$',views.BlogDetailView.as_view(),{'order_by':'pub_date'},name='blog_detail'),
	url(r'^blog/djangoins/$',views.blog_django_ins_view,name="blog_django_ins_view"),
	url(r'^blog/python/$',views.blog_python_view,name="blog_python_view"),
	url(r'^blog/zhuanzai/$',views.blog_zhuanzai_view,name="blog_zhuanzai_view"),
	url(r'^blog/yuanchuang/$',views.blog_yuanchuang_view,name="blog_yuanchuang_view"),
	url(r'^$',views.IndexView.as_view(),name='index'),
]