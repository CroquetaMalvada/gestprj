from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from gestprj import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gestprjsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^llista_projectes/', views.list_projectes, name='llista_projectes'),
    url(r'^projecte_nou/', views.new_project, name='projecte_nou'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^thanks/$', TemplateView.as_view(template_name="gestprj/thanks.html"), name='thanks'),
    url(r'^menu/$', TemplateView.as_view(template_name="gestprj/menu.html"), name='menu'),
)