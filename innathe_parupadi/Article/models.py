from django.db import models

# Create your models here.
class Article(models.Model):
    newsid = models.IntegerField()
    title = models.CharField(max_length = 9000)
    author = models.CharField(max_length = 1000)
    pubdate = models.DateTimeField()
    headpic = models.ImageField(upload_to="")
    content = models.TextField()