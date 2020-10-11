from django.urls import path, include
from . import views
from .feeds import LatestPostsFeed
from django_filters.views import FilterView
from django.views.generic import TemplateView
from django.conf.urls import url
from .filters import UserFilter
from .views import UpdatePostView,DeletePostView,AddCategoryView,LikeView

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
        template_name='blog/post/user_filter.html'), name='searching'),

    path('like/', views.image_like, name='like'),
    path('post-upload/', views.post_upload, name='post-upload'),
    path('<int:pk>/update/',UpdatePostView.as_view(),name='update_post'),
    path('<int:pk>/delete/',DeletePostView.as_view(),name='delete_post'),
    path('add_category/',AddCategoryView.as_view(),name='add-category'),
    path('category/<str:cats>/',views.CategoryView,name='category'),
    # path('category-details/',views.Categorydetails,name='category-details'),
    path('like/<int:pk>/',views.LikeView,name='like_post'),
    path('politics/',views.PoliticsView,name='politics'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('user_activity/', views.user_activity, name='user_activity'),


    



]
