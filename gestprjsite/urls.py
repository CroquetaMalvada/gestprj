from django.conf.urls import patterns, include, url
from django.contrib import admin
from gestprj import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gestprjsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^llista_projectes/', views.list_projectes, name='llista_projectes'),
)
