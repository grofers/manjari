from django.conf.urls import url, include
from django.contrib.auth.models import User

from . import views

urlpatterns = [
    url(r'^home/$', views.home),
]
