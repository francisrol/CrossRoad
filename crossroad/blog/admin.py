from django.contrib import admin
from django.db import models
from django import forms
from blog.models import Blog,BlogType
from pagedown.widgets import AdminPagedownWidget
# Register your models here.
#class BlogForm(forms.ModelForm):

 #   class meta:
 #       model = Blog


class BlogAdmin(admin.ModelAdmin):
    #form = BlogForm
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    fieldsets = [
    	('标题',				{"fields":['title']}),
    	('分类',				{"fields":['blogtype']}),
    	('摘要',				{"fields":['summary']}),
    	('内容',				{"fields":['content']}),
    	('日期',             {"fields":['pub_date']}),
    ]

    search_fields = ['title','summary']
    list_display = ('title','pub_date')
    list_filter = ['title','blogtype']
    
class BlogTypeAdmin(admin.ModelAdmin):
	fieldsets = [
		('标题',				{"fields":['btype']}),
        ('别名',              {"fields":['alias']}),
	]
	list_display = ('btype','alias','id')

admin.site.register(Blog,BlogAdmin)
admin.site.register(BlogType,BlogTypeAdmin)