from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy as _
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import CreateView
from .models import Article, Tag, Category, Comment

def categories(request):
	return {
		'categories':Category.objects.all(),
	}

class ArticleList(ListView):
	model = Article
	template_name = 'blog/index.html'
	paginate_by = 3

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = "Blog"
		return context
	
	def get_queryset(self):
		return Article.objects.filter(status='published')
	

# class ArticleDetail(DetailView):
# 	model = Article
# 	template_name = 'blog/article_detail.html'

def post_detail(request, slug):
	post = get_object_or_404(Article, slug=slug, status='published')
	get_comment = post.comments.filter(status= True)
	page = request.GET.get('page', 1)
	paginator  = Paginator(get_comment, 4)

	try:
		comments = paginator.page(page)
	except PageNotAnInteger:
		comments = paginator.page(1)
	except EmptyPage:
		comments = paginator.page(num_pages)

	user_comment = None

	if request.method=='POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			user_comment =  comment_form.save(commit = False)
			user_comment.post = post
			user_comment.save()
			return HttpResponseRedirect('/article/' + post.slug)
	else:
		comment_form = comment_form()
	context = {
		'post': post, 
		'comment_form': comment_form,
		'get_comment':get_comment,
		'comments': user_comment,
		'comments': comments, 
		'title': post.title
		}
	return render(request, 'blog/article_detail.hmtl', context)

class AddArticle(LoginRequiredMixin, CreateView):
	model = Article
	template_name = 'blog/add_article.html'
	success_url = _('article_detail')

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.instance.slug = slugify(form.instance.title)
		return super(AddArticle, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Create New Article'
		return context
	
class ArticleUpdate(UpdateView):
	model = Article
	template_name = "blog/article_edit.html"
	success_url = _('article_detail')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(ArticleUpdate, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Edit Article'
		return context
	
	def test_func(self):
		post = self.get_object()
		if self.request.user == author:
			return True
		return False

class DeleteArticle(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Article
	template_name = 'blog/article_delete.html'
	success_url = _('blog')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Delete Article'
		return context
	
	def test_func(self):
		post = self.get_object()
		if self.request.user == author:
			return True
		return False
	
class CommentUpdate(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
	model = Comment
	fields = ['body', 'status']
	success_url = _('article_detail')

	def form_valid(self, form):
		form.instance.post = self.post
		return super(CommentUpdate, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Update a Comment'
		return context

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.user:
			return True
		return False


class CommentDelete(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
	model = Comment
	context_object_name = 'comment'
	success_url = _('article_detail')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Delete a Comment'
		return context

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.user:
			return True
		return False

def category_list(request,category_slug):
    category=get_object_or_404(Category, slug = category_slug)
    posts=Post.objects.filter(category = category)
    context={'category':category, 'posts':posts, 'title':category.name}
    return render(request, 'posts/category.html', context)