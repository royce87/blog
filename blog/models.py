from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    text = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text
