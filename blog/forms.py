from django import forms
from .models import Article

class NewArticle(forms.ModelForm):
	title = forms.CharField(
		widget= TextInput(
			attrs= {'placeholder': 'Input the title'}
			)
		max_length= 255,
		help_text= 'Max length of title is 255',
		)
	content = forms.CharField(
		widget= TextArea(
			attrs={'placeholder': 'What\'s on Your Mind?'}
			),
		)
	category=forms.ModelChoiceField(queryset=Category.objects.all(),required=True)
	status=forms.CharField(widget=forms.Select(choices=Post.options),required=True)
	class Meta:
		model= Article
		fields = ['title', 'content', 'category', 'status']


class CommentForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your name'}),required=True)
	email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Your email'}), help_text='Your email will not be published.', required=True)
	text = forms.CharField(widget= froms.Textarea(attrs={'placeholder':'Your Comment'}),required=True)
	
	class Meta:
		model = Comment
		fields = ("name", "email", "text")
