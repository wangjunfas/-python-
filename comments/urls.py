from django.conf.urls import url

from .views import post_comment

app_name = 'comments'

urlpatterns = [
    url(r'^post_comment/(?P<pk>\d+)/$', post_comment, name='post_comment'),
]