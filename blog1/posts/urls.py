
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import UserFormView
from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    comment_create,
    user_login,
    user_logout,
)
urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^register/$', UserFormView.as_view(), name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^create/$', post_create, name='create'),
    url(r'^(?P<pk>\d+)/add-comment/$', comment_create, name='add-comment'),
    url(r'^(?P<pk>\d+)/$', post_detail, name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', post_update, name='update'),
    url(r'^(?P<pk>\d+)/delete$', post_delete),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)