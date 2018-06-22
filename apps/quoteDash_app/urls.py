from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.validate_login),
    url(r'^quotes$', views.success),
    url(r'^addquote$', views.addquote),
    url(r'^myaccount/(?P<id>\d+)$', views.editMyaccountPage),
    url(r'^user/(?P<id>\d+)$', views.userPage),
    url(r'^updateAccount$', views.updateAccount),
    url(r'^delete_quote/(?P<id>\d+)$', views.delete_quote),
    url(r'^likequote/(?P<id>\d+)$', views.like_quote),
    url(r'^logout$', views.logout),
]           