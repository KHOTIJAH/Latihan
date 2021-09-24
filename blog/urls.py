from django.urls import path
from .views import ArticleList

urlpatterns = [
	path('', ArticleList.as_view(), name= 'blog'),
	# path('article/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
]