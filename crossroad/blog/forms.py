from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django import forms
#注册表单
class RegisterForm(forms.Form):
	username = forms.CharField(label='用户名')
	password = forms.CharField(label='登录密码',widget=forms.PasswordInput)
	password2 = forms.CharField(label='确认密码',widget=forms.PasswordInput)
	email = forms.EmailField(label='邮箱')
	#当类实例调用.is_valid()方法时，clean方法自动被调用，进行过滤，检验表单数据是否符合要求
	def clean(self):
		cleaned_data = super(RegisterForm,self).clean()
		username = cleaned_data.get('username')
		password = cleaned_data.get("password")
		password2 = cleaned_data.get("password2")

		if password != password2:
			msg = "密码输入不一致，请重新输入!"
			self.add_error('password2',msg)
		try:
			u = User.objects.get(username=username)
		except:
			u = None
		if u:
			msg = "该用户已存在！"
			self.add_error('username',msg)
#登录表单
class LoginForm(forms.Form):
	username = forms.CharField(label='用户名')
	password = forms.CharField(label='登录密码',widget=forms.PasswordInput)
	#当类实例调用.is_valid()方法时，clean方法自动被调用，进行过滤，检验表单数据是否符合要求
	def clean(self):
		cleaned_data = super(LoginForm,self).clean()
		username = cleaned_data.get('username')
		password = cleaned_data.get("password")

		user = authenticate(username=username,password=password)
		if user is None:
			msg = "用户名或密码有误，请重新输入！"
			self.add_error('username',msg)

#更改密码表单
class PwChangeForm(forms.Form):
	username = forms.CharField(disabled=True)
	
	password = forms.CharField(label='原密码',widget=forms.PasswordInput)
	new_password = forms.CharField(label='新密码',widget=forms.PasswordInput)
	new_password2 = forms.CharField(label='确认新密码',widget=forms.PasswordInput)
	#当类实例调用.is_valid()方法时，clean方法自动被调用，进行过滤，检验表单数据是否符合要求
	def clean(self):
		cleaned_data = super(PwChangeForm,self).clean()
		username = cleaned_data.get('username')
		password = cleaned_data.get("password")

		user = authenticate(username=username,password=password)
		if user is None:
			msg = "密码错误，请重新输入！"
			self.add_error('password',msg)
		elif new_password != new_password2:
			msg = "密码输入不一致，请重新输入!"
			self.add_error('new_password',msg)