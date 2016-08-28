from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
	url(r'^register/$',views.register_view,name='register'),
	url(r'^login/$',views.login_view,name='login'),
	url(r'^logout/$',views.logout_view,name='logout'),

	url(r'^accounts/change-password/$',views.password_change,name='pw_change'),
	url(r'^accounts/reset-password/$',views.password_reset,name='password_reset'),
	url(r'^accounts/reset-password-done/$',views.password_reset_done,name='password_reset_done'),
	url(r'^accounts/reset-password-confirm/(?P<uidb64>[0-9a-zA-Z]+)/(?P<token>[0-9a-zA-Z\-]+)/$',views.password_reset_confirm,name='password_reset_confirm'),
	url(r'^accounts/reset-password-complete/$',views.password_reset_complete,name='password_reset_comlete'),

	url(r'^accounts/profile/(?P<pk>[0-9]+)/$',views.ProfileView.as_view(),name='profile'),
	url(r'^accounts/profile-edit/(?P<pk>[0-9]+)/$',views.ProfileEditView.as_view(),name='profile_edit'),

	#url(r'^blog/([\w-]+)/$',views.BlogDetailView.as_view(),name='blog_type_list'),
	url(r'^blog/(?P<alias>[\w-]+)/(?P<pk>[0-9]+)/$',views.BlogDetailView.as_view(),{'order_by':'pub_date'},name='blog_detail'),

	url(r'^blog/djangoins/$',views.blog_django_ins_view,name="blog_django_ins_view"),
	url(r'^blog/python/$',views.blog_python_view,name="blog_python_view"),
	url(r'^blog/zhuanzai/$',views.blog_zhuanzai_view,name="blog_zhuanzai_view"),
	url(r'^blog/yuanchuang/$',views.blog_yuanchuang_view,name="blog_yuanchuang_view"),

	url(r'^$',views.IndexView.as_view(),name='index'),
]