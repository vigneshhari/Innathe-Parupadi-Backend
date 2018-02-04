from django.shortcuts import render
from django.db.models import Max
import datetime
from django.http import JsonResponse
from .models import Article , User
from django.http import HttpResponseRedirect


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
    if(request.session.get("loggedin",0) == 0 ):return HttpResponseRedirect("/")
    val = Article.objects.all().aggregate(Max("newsid"))
    Article(newsid = val["newsid__max"] + 1  , title = request.POST.get("title") , author = request.POST.get("author") , headpic = request.FILES["headpic"] , content = request.POST.get("content") , pubdate = datetime.datetime.now()).save()
    return HttpResponseRedirect("/upload/new/")

def loginview(request):
    return render(request,"login.html")

def login(request):
    for i in request.POST.keys():
        print(i,request.POST[i])
    if(User.objects.all().filter(name = request.POST.get("name") , passhash = request.POST.get("password")).__len__() == 1 ):
        request.session["loggedin"] = 1
        return HttpResponseRedirect("/upload/new/")