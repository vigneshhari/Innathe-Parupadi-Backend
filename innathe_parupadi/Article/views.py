from django.shortcuts import render
from django.db.models import Max
import datetime
from django.http import JsonResponse
from .models import Article , User
from django.http import HttpResponseRedirect

def my_login_required(View):
    def wrapper(request, *args, **kw):
        user=request.user  
        if request.session.get("loggedin","0") == 0:
            return HttpResponseRedirect('/')
        else:
            return View(request, *args, **kw)
    return wrapper


def article(request):
    if("id" not in request.GET.keys()):return JsonResponse({"Response Code" : "400"})
    if(len(Article.objects.all().filter(id = request.GET.get("id"))) != 1 ):return JsonResponse({"Response Code" : "404"})
    articleobj = Article.objects.get(id = request.GET.get("id"))
    return JsonResponse({"title" : articleobj.title , "author" : articleobj.author , "picurl" : articleobj.headpic.url , "Date" : articleobj.pubdate , "content" : articleobj.content})

def listarticles(request):
    data = Article.objects.all()
    lis = []
    for i in data:
        lis.append({"title" : i.title , "picurl" : i.headpic.url , "author" : i.author,"newsid" : i.newsid})
    return JsonResponse({"data" : lis})

@my_login_required
def add(request):
    val = request.session.get("edit",-1)
    if(val == -1):
        request.session.get("create",-1)
    if(request.POST.get("headpic").strip() == ""):
        Article.objects.filter(newsid = val).update( title = request.POST.get("title") , author = request.POST.get("author") , content = request.POST.get("content") )
    else:
        Article.objects.filter(newsid = val).update( title = request.POST.get("title") , author = request.POST.get("author") , headpic = request.FILES["headpic"] , content = request.POST.get("content") )
    return HttpResponseRedirect("/news/dash/")

def loginview(request):
    return render(request,"login.html")

def login(request):
    for i in request.POST.keys():
        print(i,request.POST[i])
    if(User.objects.all().filter(username = request.POST.get("name") , passhash = request.POST.get("password")).__len__() == 1 ):
        request.session["loggedin"] = 1
        request.session["userid"] = User.objects.get(username = request.POST.get("name") , passhash = request.POST.get("password")).id
        return HttpResponseRedirect("/news/dash")
    else:
        return HttpResponseRedirect("/")

def logout(request):
    request.session["loggedin"] = 0
    request.session["userid"] = -1
    return HttpResponseRedirect("/")

@my_login_required
def dash(request):
    Articles = Article.objects.all().filter(ownerid = request.session["userid"])
    name = User.objects.get(id = request.session["userid"]).name
    data = []
    for i in Articles:
        data.append({"url" : i.headpic.url , "title" : i.title , "author" : i.author , "published" : i.published , "editlink" : ("/news/edit?id=" + str(i.newsid)) })
    return render(request , "dash.html", {"name" : name , "artno" : len(Articles) , "pub" : len(Articles.filter(published = 1)) , "unpub" : len(Articles.filter(published = 0)) , "data" : data })

@my_login_required
def edit(request):
    if("id" not in request.GET.keys()):return HttpResponseRedirect("/")
    if(Article.objects.get(newsid = request.GET.get("id")).ownerid != request.session["userid"]):return HttpResponseRedirect("/")
    request.session["edit"] = request.GET.get("id")
    request.session["create"] = -1
    return HttpResponseRedirect("/upload/new")

@my_login_required
def createnew(request):
    val = Article.objects.all().aggregate(Max("newsid"))
    Article(newsid = val , ownerid = request.session["userid"] , published = 0).save()
    

@my_login_required
def pub(request):
    val = request.session.get("edit",-1)
    if(val == -1):
        request.session.get("create",-1)
    if("id" not in request.GET.keys()):return HttpResponseRedirect("/")
    if(Article.objects.get(newsid = request.GET.get("id")).ownerid != request.session["userid"]):return HttpResponseRedirect("/")
    obj = Article.objects.get(newsid = val )
    if(obj.published == 1):
        Article.objects.filter(newsid = val).update( published = 0 )
    else:
        Article.objects.filter(newsid = val).update( published = 1 , pubdate = datetime.datetime.now() )
    return HttpResponseRedirect("/upload/new")


    