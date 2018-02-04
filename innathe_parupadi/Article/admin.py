from django.contrib import admin
from .models import Article, User
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summer_note_fields = '__all__'

admin.site.register(Article , SomeModelAdmin )
admin.site.register(User)
