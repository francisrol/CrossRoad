# coding:utf-8

import hashlib

from django.db import models
from django.contrib.auth.models import User

SLUGKEY = 'crossroad'
# 文章标签 与 博客多对多关系
class BlogTags(models.Model):
    # 标签
    btag = models.CharField(max_length=31)
    # 别名 用于url
    alias = models.SlugField()

    def __str__(self):
        return self.btag

# 文章分类
class BlogCategory(models.Model):
    # 分类
    bcategory = models.CharField(max_length=31)
    # 别名 用于url
    alias = models.SlugField()
    def __str__(self):
        return self.bcategory

# 文章正文
class Blog(models.Model):

    # 文章标题
    title = models.CharField(max_length=100)
    # 文章概要
    summary = models.CharField(max_length=200)
    # 文章正文
    content = models.TextField()
    # 发表时间
    pub_date = models.DateTimeField()
    # 文章url识别字符串，一串md5值
    slug = models.SlugField(blank=True, null=True)
    # 文章标签
    blogtag = models.ManyToManyField(BlogTags)
    # 文章分类
    blogcategory = models.ForeignKey(BlogCategory)

    def save(self, *args, **kwargs):
        # 生成slug值
        md5 = hashlib.md5()
        md5.update(str(self.id).encode('utf-8'))
        md5.update(SLUGKEY.encode('utf-8'))
        self.slug = md5.hexdigest()
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title