from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from .models import Post, Comment,Category,Contact
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, \
                   UserEditForm,PostForm
# filter
from django.contrib.auth.models import User
from .filters import UserFilter

# like 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import redis
from django.conf import settings

# update post
from django.utils.decorators import method_decorator
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy,reverse
from common.decorators import ajax_required
# action
from actions.utils import create_action
from actions.models import Action


r = redis.Redis(host=settings.REDIS_HOST,
 port=settings.REDIS_PORT,
 db=settings.REDIS_DB)

@login_required
@require_POST
def image_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    print(post_id)
    print(action)

    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.user_like.add(request.user)
            else:
                post.user_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})

def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'account/user_filter.html', {'filter': user_filter})


from django.contrib.auth.models import User

# @login_required
def post_list(request, tag_slug=None):
    
    object_list = Post.published.all()
    category_details = Category.objects.all()
    # increment total image views by 1
    total_views = r.incr(f'Post:{Post.id}:views')

    geek_object = Post.objects.update(total_views = total_views)
    # geek_object.save() 
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                 'account/posts.html',
                 {'page': page,
                  'posts': posts,
                  'tag': tag,
                  'total_views': total_views,
                  'category_details':category_details,
                })

@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]

    return render(request,
                  'account/details.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts,
                   })


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'account/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

@login_required
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
            
    return render(request,
                  'account/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


@login_required
def post_upload(request):
    form_class = PostForm
    form = form_class(request.POST or None)

    if request.method == 'POST':
        # A comment was posted
        if form.is_valid():
            # Save the comment to the database
            # print (form['title'].value())
            # print (form.data['title'])
            title =form.data['title']
            form.save()
            # print(form.title)
            return render(request,
                          'account/uploadsuccess.html',{'title':title}
                          )
    else:
        form = PostForm()

    return render(request,
                  'account/uploadpost.html',
                  {'post_form':form
                    })

@method_decorator(login_required, name='dispatch')
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'account/update_post.html'
    fields = ['title','slug','body','status','tags']

@method_decorator(login_required, name='dispatch')
class DeletePostView(DeleteView):
    model = Post
    template_name = 'account/delete_post.html'

    def get_success_url(self):
        return reverse('blog:post_list')


class AddCategoryView(CreateView):
    model = Category
    template_name = 'account/add_category.html'
    fields = '__all__'



def CategoryView(request,cats):
    category_post = Post.objects.filter(category=cats.replace('_',' '))
    paginator = Paginator(category_post, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render (request,'account/categories.html',{'page':page,'cats':cats.title().replace('_',' '),'category_post':category_post,'posts':posts})


# def Categorydetails(request):
#     category_details = Category.objects.all()
#     return render(request,'base.html',{'category_details':category_details})


def LikeView(request ,pk):
    post =get_object_or_404(Post, id=request.POST.get('post_id'))
    liked=False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('blog:post_list'))
    
@login_required
def PoliticsView(request):
    post_politics =Post.objects.filter(category='politics')
    return render(request, 'account/politics.html',{'post_politics':post_politics})



# follow and u follow
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/userlist.html',
                  {'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/userdetails.html',
                  {'user': user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})


# user activity
@login_required
def user_activity(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10]

    return render(request,
                  'account/activities.html',
                  {'actions': actions})