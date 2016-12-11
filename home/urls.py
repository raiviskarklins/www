from django.conf.urls import url
from .import views

app_name = 'home'

urlpatterns = [

    # /
    url(r'^$', views.index, name='index'),

    #/(categpry_id)/
    url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(), name='category'),

    url(r'^blog/(?P<blog_pk>[0-9]+)/$', views.blogview, name='blog'),

    url(r'^login/$', views.login_user, name='login'),

    url(r'^register/$', views.register_user, name='register'),

    url(r'^logout/$', views.logout_user, name='logout'),

    url(r'^profile/(?P<pro_pk>[0-9]+)/$', views.profileview, name='profile'),

    url(r'^create_blog/$', views.add_blog, name='add_blog'),

    url(r'^user/(?P<usr_pk>[0-9]+)/$', views.userview, name='user'),

    url(r'^(?P<blog_pk>[0-9]+)/delete_blog/$', views.delete_blog, name='delete_blog'),

    url(r'^(?P<blog_pk>[0-9]+)/edit_blog/$', views.edit_blog, name='edit_blog'),

    url(r'^(?P<blog_pk>[0-9]+)/edit_blog/save/$', views.save_edit_blog, name='save_blog'),



]