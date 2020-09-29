from django.urls import path, include
from . import views
from .feeds import LatestPostsFeed
from django_filters.views import FilterView
from django.views.generic import TemplateView
from django.conf.urls import url
from .filters import UserFilter
app_name = 'blog'

urlpatterns = [
    
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('searchuser/', views.search, name='search'),
    url(r'^searching/$', FilterView.as_view(filterset_class=UserFilter,
        template_name='blog/post/user_filter.html'), name='search'),

    path('like/', views.image_like, name='like'),

]
