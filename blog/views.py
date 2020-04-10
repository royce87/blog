from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView

from .models import Post, Comment
from taggit.models import Tag
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
        posts = Post.objects.filter(tags__name__in=[tag])
        print(posts)
        return render(request, 'tag.html', {'tag': tag, 'posts': posts})


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
            bound_form.save_m2m()
        return redirect('/')


class DeletePost(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        return render(request, 'delete_post.html', {'post': post})

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if request.user == post.author:
            post.delete()
        return redirect('/')


class EditPost(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        bound_form = CreatePostForm(instance=post)
        return render(request, 'edit_post.html', {'form': bound_form, 'post': post})

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if request.user == post.author:
            bound_form = CreatePostForm(request.POST, instance=post)
            if bound_form.is_valid():
                edited_post = bound_form.save()
                return redirect(edited_post)
