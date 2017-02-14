from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Blog
from .filters import search,blog_filter


class IndexView(generic.ListView):
	model = Blog  						#显示内容的模板类
	template_name = 'blog/index.html'	#前端html模板
	paginate_by = 5						#每页条目数
	paginate_orphans = 1				#最大孤页显示条目数

	#以下为非继承的类属性
	#设置全文检索的查找范围
	search_fields = ['title','summary']
	searched = False	#判断是否经过查询
	btype_num_list = None	#对筛选结果计数后组成的一个，BlogType分类的list，作为上下文发送给前端
	btype_uri = ''	#将进行分类查询的字符串，作为上下文发送给前端，以便前端组成url

	#重写父类的get_queryset方法，
	def get_queryset(self):
		#进行字词搜索
		query_results,self.searched = search(self.request,Blog.objects.all(),self.search_fields)
		#获取分类查询的字符串，没有则为‘’
		alias_string = self.kwargs.get('btype') or self.request.GET.get('btype') or ''
		self.btype_uri = alias_string	#赋给类属性
		#进行blog分类筛选
		queryset_list,self.btype_num_list = blog_filter(query_results,alias_string)
		return queryset_list.order_by('-pub_date')
	#重写父类方法
	def get_context_data(self, **kwargs):
		#获取为处理过的上下文数据
		context = super(IndexView,self).get_context_data(**kwargs)

		#以下均为新增的上下文，以便在前端进行布局，设置超链接url等
		if self.searched:
			results_num = context['paginator'].count
			context['results_num'] = results_num
			context['form_string'] = self.request.GET.get('q','')
		context['btype_num_list'] = self.btype_num_list
		context['btype_uri'] = self.btype_uri
		return context


# #为表单html元素添加自定义属性
# def add_attrs(form):
# 	for field in form:
# 		#为<input>添加class
# 		field.field.widget.attrs.update({'class':'form-control'})
# 		#为<label>添加class
# 		field.label=field.label_tag(attrs={'class':'col-sm-2 control-label'})
# 	return form
#
# def form_data_factory(request,formclass):
# 	return formclass(request.POST)
#
# #用户注册
# def register_view(request):
#
# 	if request.method == 'POST':
# 		'''
# 		#当使用ajax提交表单时的部分代码，是我一开始尝试的方法，丧失了django自带User类的很多功能，所以弃用
# 		data = json.loads(request.body.decode('utf-8'))
# 		username = data.get('username','')
# 		password = data.get('password','')
# 		email = data.get('email','')
#
# 		try:
# 			un = User.objects.get(username=username)
# 			if un:
# 				return HttpResponse...
# 		except:
# 			return render(request,'blog/index.html',{'username':username,'email':email})
# 		'''
# 		#获取表单数据
# 		#data = request.POST
# 		#将数据bound到Form类实例，以便进行检验操作
# 		post_form = form_data_factory(request,RegisterForm)	#RegisterForm(data)
# 		#检验表单数据是否符合要求
# 		if post_form.is_valid():
# 			#通过检验，创建用户
# 			user = User.objects.create_user(username=request.POST['username'],\
# 											password=request.POST['password'],\
# 											email=request.POST['email'])
# 			user.save()
# 			return redirect("blog:index")
# 		else:
# 			#未通过检验，打回重写
# 			return render(request,'blog/auth.html',{'form':add_attrs(post_form),'pagetitle':'用户注册',\
# 				'submit':'注册'})
# 	context = {'form':add_attrs(RegisterForm()),\
# 				'pagetitle':'用户注册',\
# 				'submit':'注册'}
# 	return render(request,'blog/auth.html',context)
# #用户登录
# '''
# def login_view(request):
# 	if request.user.is_authenticated:
# 		return HttpResponseRedirect(reverse("blog:index"))
# 	if request.method == 'POST':
# 		form = form_data_factory(request,LoginForm)
# 		if form.is_valid():
# 			user = authenticate(username=request.POST['username'],password=request.POST['password'])
# 			login(request,user)
# 			return redirect("blog:index")
# 		else:
# 			return render(request,'blog/auth.html',{'form':add_attrs(form),'pagetitle':'用户登录',\
# 				'submit':'登录'})
# 	context = {'form':add_attrs(LoginForm()),\
# 				'pagetitle':'用户登录',\
# 				'submit':'登录'}
# 	return render(request,'blog/auth.html',context)
# '''
#
# #使用django原生方法进行操作，注释里为为使用原生方法进行的相同操作，下同
# def login_view(request):
# 	template_response = views.login(request,\
# 			template_name='blog/registration/login.html'
# 			)
# 	return template_response
#
# '''
# def logout_view(request,uid):
# 	user = get_object_or_404(User,pk=uid)
# 	if request.user.is_authenticated:
# 		logout(request)
# 	return redirect("blog:index")
# '''
# def logout_view(request):
# 	template_response = views.logout(request,\
# 			template_name='blog/registration/logged_out.html'
# 			)
# 	return template_response
#
# '''
# @login_required
# def password_change(request,uid):
# 	u = get_object_or_404(User,pk=uid)
# 	#确认是否为当前登录的用户
# 	if request.user != u:
# 		return HttpResponseNotFound
# 	else:
# 		if request.method == 'POST':
# 			form = form_data_factory(request,PwChangeForm)
# 			if form.is_valid():
# 				user = request.user
# 				user.set_password(request.POST['new_password'])
# 				user.save()
# 				logout(request)
# 				return redirect("blog:login")
# 			else:
# 				return render(request,'blog/auth.html',{'form':add_attrs(form)})
# 		context = {'form':add_attrs(PwChangeForm({'username':request.user.username})),\
# 					'pagetitle':'修改密码',\
# 					'submit':'提交'}
# 		return render(request,'blog/auth.html',context)
# '''
# #使用django原生方法进行操作
# def password_change(request):
# 	template_response = views.password_change(request,\
# 			template_name='blog/registration/password_change_form.html',\
# 			post_change_redirect=reverse('blog:index'),\
# 			#password_change_form=add_attrs(PwChangeForm)
# 			)
# 	return template_response
# #使用django原生方法进行操作
# def password_reset(request):
# 	template_response = views.password_reset(request,\
# 			template_name='blog/registration/password_reset_form.html',\
# 			email_template_name='blog/registration/password_reset_email.html',\
# 			subject_template_name='blog/registration/password_reset_subject.txt',
# 			post_reset_redirect=reverse('blog:index'))
# 	return template_response
# #使用django原生方法进行操作
# def password_reset_done(reauest):
# 	template_response = views.password_reset(request,\
# 			template_name='blog/registration/password_reset_done.html')
# 	return template_response
# #使用django原生方法进行操作
# def password_reset_confirm(request,**kwargs):
# 	uidb64 = kwargs.get('uidb64')
# 	token = kwargs.get('token')
# 	template_response = views.password_reset_confirm(request,uidb64=uidb64,token=token,\
# 			template_name='blog/registration/password_reset_confirm.html',\
# 			set_password_form=SetPasswordForm,\
# 			post_reset_redirect=reverse('blog:index'))
# 	return template_response
# #使用django原生方法进行操作
# def password_reset_complete(request):
# 	template_response = views.password_reset_complete(request,\
# 			template_name='blog/registration/password_reset_complete.html')
# 	return template_response

# class ProfileView(generic.DetailView):
# 	model = User
# 	template_name = 'blog/profile.html'
#
# #使用django的UpdateView构建个人资料视图函数
# class ProfileEditView(generic.edit.UpdateView):
# 	model = User
# 	fields = ['email','first_name','last_name']		#可修改的项
# 	template_name = 'blog/auth.html'
# 	success_url = '/'			#成功后重定向的页面
#
# 	def get_form(self):
# 		form = super(ProfileEditView,self).get_form()
# 		#为form添加class属性
# 		return add_attrs(form)
#
# 	def get_context_data(self,**kwargs):
# 		context = super(ProfileEditView,self).get_context_data(**kwargs)
# 		context['pagetitle'] = '编辑资料'
# 		context['submit'] = '保存'
# 		return context
# 	#确保非本用户修改资料
# 	@login_required
# 	def get(self,request,pk):
# 		if self.get_object() != request.user:
# 			messages.add_message(request, messages.INFO, '请勿试图修改他人资料。')
# 			return HttpResponseRedirect(reverse('blog:index'))
# 		return super().get(request,pk)
# 	#万一非本用户提交了表单，所以再上个保险
# 	@login_required
# 	def post(self,request,pk):
# 		if self.get_object() != request.user:
# 			messages.add_message(request, messages.INFO, '请勿试图修改他人资料。')
# 			return HttpResponseRedirect(reverse('blog:index'))
# 		return super().post(request,pk)

#博客分类视图
class BlogDetailView(generic.DetailView):
	model = Blog
	template_name = 'blog/blog_detail.html'	

	search_fields = ['title','content']
	searched = False

	#重写父类get_context_data方法
	def get_context_data(self,**kwargs):
		#获取为处理过的上下文数据
		order_by = self.kwargs.get('order_by')
		context = super(BlogDetailView,self).get_context_data(**kwargs)
		#以下均为新增的上下文，以便在前端进行布局，设置超链接url等
		alias = self.kwargs.get('alias')
		query_results,self.searched = search(self.request,Blog.objects.filter(blogtype__alias=alias),\
				self.search_fields)
		querysets = query_results.order_by(order_by)
		if self.searched:
			results_num = querysets.count()
			context['results_num'] = results_num
			context['form_string'] = self.request.GET.get('q','')	
		context['object_list'] = querysets
		return context
#显示django实例教程文章的视图，
#重定向到blog_detail视图，使用其模板
#默认显示最旧的，排序为'pub_date'
def blog_django_ins_view(request):
	alias = 'djangoins'
	blog_id = Blog.objects.filter(blogtype__alias=alias).order_by('-pub_date').last().id
	return HttpResponseRedirect(reverse('blog:blog_detail',kwargs={'alias':alias,
												'pk':blog_id}))
#显示关于pythonde 文章的视图，
#重定向到blog_detail视图，使用其模板
#默认显示最新的那篇，排序为'-pub_date'												
def blog_python_view(request):
	alias = 'python'
	blog_id = Blog.objects.filter(blogtype__alias=alias).order_by('-pub_date').first().id
	return HttpResponseRedirect(reverse('blog:blog_detail',kwargs={'alias':alias,
												'pk':blog_id}))
#显示原创文章的视图，
def blog_yuanchuang_view(request):
	alias = 'yuanchuang'
	blog_id = Blog.objects.filter(blogtype__alias=alias).order_by('-pub_date').first().id
	return HttpResponseRedirect(reverse('blog:blog_detail',kwargs={'alias':alias,
												'pk':blog_id}))
#显示转载 文章的视图，
def blog_zhuanzai_view(request):
	alias = 'zhuanzai'
	blog_id = Blog.objects.filter(blogtype__alias=alias).order_by('-pub_date').first().id
	return HttpResponseRedirect(reverse('blog:blog_detail',kwargs={'alias':alias,
												'pk':blog_id}))



