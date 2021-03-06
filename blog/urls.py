from django.urls import path
# internals
from . import views
from blog.feed import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post-list'),
    path('drafts', views.drafts, name='drafts'),
    path('new/', views.PostCreateView.as_view(), name='post-create'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/',
         views.post_list, name='post-list-by-tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.post_detail, name='post-detail'),
    path('<int:post_id>/share/', views.post_share, name='post-share'),
    path('feed/', LatestPostsFeed(), name='posts-feed'),
    path('search/', views.post_search, name='post-search'),
]
