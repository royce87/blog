from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView

from .models import Post, Tag, Comment
from .forms import CommentForm, CreatePostForm


def index(request):
    return render(request, 'index.html')


def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_id)
        if request.user == comment.author:
            comment.delete()
            return redirect(comment.post.get_absolute_url())


class Home(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-date_published')
        return render(request, 'index.html', {'posts': posts})


class PostDetail(View):
    def get(self, request, post_slug, **kwargs):
        post = Post.objects.get(slug=post_slug)
        form = CommentForm()
        return render(request, 'post_detail.html', {'post': post, 'form': form})

    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post_id = Post.objects.get(slug=kwargs.get('post_slug')).id
            form.author = request.user
            form.text = request.POST.get('text')
            form.save()
        return redirect(request.path)


class TagPosts(View):
    def get(self, request, tag_slug):
        tag = Tag.objects.get(slug=tag_slug)
        return render(request, 'tag.html', {'tag': tag})


class CreatePost(View):
    def get(self, request):
        form = CreatePostForm
        return render(request, 'create_post.html', {'form': form})

    def post(self, request):
        bound_form = CreatePostForm(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
        return redirect('/')