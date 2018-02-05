# encoding: utf-8
import json

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView
from .models import Picture
from .response import JSONResponse, response_mimetype
from .serialize import serialize
from django.http import HttpResponseRedirect
from Article.models import Article
from django.utils.decorators import method_decorator

def class_view_decorator(function_decorator):

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator

def my_login_required(View):
    def wrapper(request, *args, **kw):
        user=request.user  
        if request.session.get("loggedin","0") == 0:
            return HttpResponseRedirect('/')
        else:
            return View(request, *args, **kw)
    return wrapper

@class_view_decorator(my_login_required)
class PictureCreateView(CreateView):
    model = Picture
    data="Publish"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(PictureCreateView, self).get_context_data(**kwargs)
        

        if(self.request.session.get("edit",-1) == -1):
            context['editor'] = "Replace This Text with News Content"
        else:
            val = self.request.session.get("edit",-1)
            if(val == -1):
                val = self.request.session.get("create",-1)
            print(val)
            Article_obj = Article.objects.get(newsid = val)
            context['title'] = Article_obj.title
            context['author'] = Article_obj.author
            context['editor'] = Article_obj.content
            context["published"] = Article_obj.published
            context["url"] = "/news/pub?id=" + str(self.request.session["edit"])

        return context

    def form_valid(self, form):
        test = form.cleaned_data
        val = self.request.session.get("edit",-1)
        if(val == -1):
            val = self.request.session.get("create",-1)
        self.object = Picture(file = test["file"] , newsid = val)
        self.object.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')



class AngularVersionCreateView(PictureCreateView):
    template_name_suffix = '_angular_form'



class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(ListView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        val = self.request.session.get("edit",-1)
        if(val == -1):
            val = self.request.session.get("create",-1)
        files = [ serialize(p) for p in Picture.objects.all().filter(newsid = val) ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
