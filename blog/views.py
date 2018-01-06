from django.shortcuts import render, get_object_or_404
from blog.models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from blog.forms import EmailPostForm, CommentForm, Searchform
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count, Q

from haystack.query import SearchQuerySet

# Create your views here.

# basic views(выполняет все теже функции что и post_list(только в
# lists.html нужно заменить  with page=posts %} на with page=page.obj
# и в urls.py приложения заменить url(r'^$', views.post_list, name='post_list'),
# на url(r'^$', views.PostListView.as_view(), name='post_list'),
# class PostListView(ListView):
# queryset = Post.published.all()
# context_object_name = 'posts'
# paginate_by = 3
# template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    #search form
    query = request.GET.get('q')
    if query:
        object_list = object_list.filter(Q(title__icontains=query) |
                                         Q(body__icontains=query)
                                         ).distinct()
    #Pagination pages
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',
                  {'posts': posts,
                   'page': page,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but dont save to database
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    # list of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
        .order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # ...send email
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'. \
                format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'. \
                format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'kriboco@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

    # posts = Post.published.all()

def about_page(request):
    return render(request, 'blog/post/about.html')

def projects_list(request):
    return render(request, 'blog/post/projects.html')