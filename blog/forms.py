from django import forms
from .models import Comment, Post
from taggit.forms import TagWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        labels = {'text': 'Comment text'}
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control p-0'})}


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'text', 'tags']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control p-0'}),
                   'slug': forms.TextInput(attrs={'class': 'form-control p-0'}),
                   'text': forms.TextInput(attrs={'class': 'form-control p-0'}),
                   'tags': TagWidget(attrs={'class': 'form-control p-0'})}
