from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'article/',views.article , name='article'),
    url(r'list/',views.list , name='list'),

    ]