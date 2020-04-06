from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='index_url'),
    path('post/<slug:post_slug>/', views.PostDetail.as_view(), name='post_detail_url'),
    path('tag/<slug:tag_slug>', views.TagPosts.as_view(), name='tag_detail_url'),
    path('delete-comment/<int:comment_id>', views.delete_comment, name='delete-comment'),
]