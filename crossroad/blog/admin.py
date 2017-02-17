from django.contrib import admin
from django.db import models
from django import forms
from blog.models import Blog, BlogTags, BlogCategory
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
    	('标题',	{"fields":['title']}),
        ('摘要', {"fields": ['summary']}),
        ('内容', {"fields": ['content']}),
    	('标签',	{"fields":['blogtag']}),
    	('分类',	{"fields":['blogcategory']}),
    	('日期', {"fields":['pub_date']}),
    ]

    search_fields = ['title','summary']
    list_display = ('title','pub_date', 'slug')
    list_filter = ['title','blogtag']

class BlogTagsAdmin(admin.ModelAdmin):
    fieldsets = [
    	('Tag',				{"fields":['btag']}),
        ('别名',              {"fields":['alias']}),
	]
    list_display = ('btag','alias','id')

class BlogCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
    	('Category',				{"fields":['bcategory']}),
        ('别名',              {"fields":['alias']}),
	]
    list_display = ('bcategory','alias','id')

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogTags, BlogTagsAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)