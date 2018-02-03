from django.shortcuts import render
from django.db.models import Max
import datetime
from django.http import JsonResponse
from .models import Article

def article(request):
    if("id" not in request.GET.keys()):return JsonResponse({"Response Code" : "400"})
    if(len(Article.objects.all().filter(id = request.GET.get("id"))) != 1 ):return JsonResponse({"Response Code" : "404"})
    articleobj = Article.objects.get(id = request.GET.get("id"))
    return JsonResponse({"title" : articleobj.title , "author" : articleobj.author , "picurl" : articleobj.headpic.url , "Date" : articleobj.pubdate , "content" : articleobj.content})

def list(request):
    data = Article.objects.all()
    lis = []
    for i in data:
        lis.append({"title" : i.title , "picurl" : i.headpic.url , "author" : i.author,"newsid" : i.newsid})
    return JsonResponse({"data" : lis})

def add(request):
    val = Article.objects.all().aggregate(Max("newsid"))
    Article(newsid = val["newsid__max"] + 1  , title = request.POST.get("title") , author = request.POST.get("author") , headpic = request.FILES["headpic"] , content = request.POST.get("content") , pubdate = datetime.datetime.now()).save()
    for i in request.POST.keys():
        print(i , " " ,request.POST[i])