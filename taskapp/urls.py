"""todo_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework.routers import DefaultRouter

from doit.views import TaskViewSet
from authentication.views import AccountViewSet
from authentication.views import LoginView
from authentication.views import LogoutView


router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'users', AccountViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^user/sessions/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]
