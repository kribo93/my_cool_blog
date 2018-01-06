from django.conf.urls import url
from . import views
from blog.feeds import LatestPostFeed
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    #url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share,
        name='post_share'),
    url(r'^feed/$', LatestPostFeed(), name='post_feed'),
    url(r'^about/$', views.about_page, name='about_page'),
    url(r'^projects/$', views.projects_list, name='projects_list'),
]
