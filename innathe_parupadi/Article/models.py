from django.db import models

# Create your models here.
class Article(models.Model):
    newsid = models.IntegerField()
    ownerid = models.IntegerField()
    title = models.CharField(max_length = 9000,blank=True,null=True)
    author = models.CharField(max_length = 1000,blank=True,null=True)
    pubdate = models.DateTimeField(blank=True,null=True)
    headpic = models.ImageField(upload_to="",blank=True,null=True)
    content = models.TextField(blank=True,null=True)
    published = models.IntegerField() # 0 is UnPublished , 1 is Published

class User(models.Model):
    username = models.CharField(max_length = 1000)
    passhash = models.CharField(max_length = 1000)
    name = models.CharField(max_length = 1000)