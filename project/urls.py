"""newproject URL Configuration

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
from django.contrib import admin
import newapp.views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', newapp.views.home, name='home'),
    url(r'^game/(?P<slug>[\w\:\s\-\+]+)/$', newapp.views.game),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^logout', newapp.views.logout_view, name='logout'),
    url(r'^favorites', newapp.views.favorites, name='favorites'),
    url(r'^recent', newapp.views.recent, name='recent'),
    url(r'^delete', newapp.views.delete, name='delete'),
    url(r'^add', newapp.views.add, name='add'),
    url(r'^external', newapp.views.external, name='external'),
]



