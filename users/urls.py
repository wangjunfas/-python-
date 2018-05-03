from django.conf.urls import url
from .views import register

app_name = 'users'

urlpatterns = [
    url(r'^register/$', register, name='register'),
]