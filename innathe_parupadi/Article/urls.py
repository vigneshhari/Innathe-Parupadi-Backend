from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'article/',views.article , name='article'),
    url(r'list/',views.listarticles , name='list'),
    url(r'add/',views.add , name='add'),
    url(r'login/',views.login , name='login'),
    url(r'logout/',views.logout , name='logout'),
    url(r'dash/',views.dash , name='dash'),
    url(r'edit/',views.edit , name='edit'),
    url(r'pub/',views.pub , name='pub'),
    url(r'createnew/',views.createnew , name='createnew'),

    ]