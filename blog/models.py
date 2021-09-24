from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length= 50, unique= True)
	slug = models.SlugField(unique= True, null= True)
	created = models.DateTimeField(auto_now_add= True, null= True)
	updated = models.DateTimeField(auto_now= True, null= True)

	class Meta:
		verbose_name_plural = 'Categories'

	def get_absolute_url(self):
		return reverse("category_list", args=[self.slug])
	
	def __str__(self):
		return str(self.name)
   
class Tag(models.Model):
	name = models.CharField(max_length= 50, unique= True)
	slug = models.SlugField(unique= True, null= True)
	created = models.DateTimeField(auto_now_add= True, null= True)
	updated = models.DateTimeField(auto_now= True, null= True)

	def __str__(self):
		return str(self.name)

class Article(models.Model):
	STATUS =(
		('draft', 'Draft'),
		('publish', 'Published'),
	)

	title = models.CharField(max_length= 255, unique= True, help_text='Please do not exceed 255 characters')
	slug = models.SlugField(unique= True)
	author = models.ForeignKey(User, on_delete= models.DO_NOTHING)
	category = models.ForeignKey(Category, on_delete= models.SET('Uncategorized'), default=1)
	tag = models.ManyToManyField(Tag)
	created = models.DateTimeField(auto_now_add= True, null= True)
	updated = models.DateTimeField(auto_now= True, null= True)
	content = models.TextField(null= True)
	status = models.CharField(max_length= 10, choices=STATUS, default='draft')
	view = models.BigIntegerField(default=0)
	comment = models.BigIntegerField(default=0)

	class Meta:
		ordering = ['-created']

	def get_absolute_url(self):
		return reverse("article_detail", args= [self.slug])
	

	def __str__(self):
		return str(self.title)

	def viewed(self):
		self.view += 1
		self.save(update_fields=['view'])

	def commented(self):
		self.comment += 1
		self.save(update_fields=['comment'])
    
class Comment(models.Model):
	post = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE, blank= True, null= True)
	user = models.CharField('User Comment', max_length=80, null= True)
	text = models.TextField(verbose_name='Comment Body', null= True)
	create_time = models.DateTimeField(auto_now_add=True, null= True)
	email = models.CharField(max_length=200, null= True)
	status = models.BooleanField(default=False)

	class Meta:
		ordering = ['-create_time']

	def __str__(self):
		return f"{self.name}'s comment on {self.post}"