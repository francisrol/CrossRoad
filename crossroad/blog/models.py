from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogType(models.Model):
	btype = models.CharField(max_length=100)
	alias = models.CharField(max_length=100)

	def __str__(self):
		return self.btype

class Blog(models.Model):

	title = models.CharField(max_length=100)
	summary = models.CharField(max_length=200)
	content = models.TextField()
	pub_date = models.DateTimeField()
	blogtype = models.ManyToManyField(BlogType)

	def __str__(self):
		return self.title