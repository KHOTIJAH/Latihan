from django.contrib import admin
from .models import Category, Tag, Comment, Article
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
	prepopulated_fields= {'slug':('title',)}

class TagAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
admin.site.register(Article, ArticleAdmin)