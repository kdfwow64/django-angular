"""URLs for risk app."""
from django.urls import include, re_path
from .views import home, auth, dashboard


urlpatterns = [
    re_path(r'^auth/signin/$', auth.signin, name='auth_signin'),
    re_path(r'^auth/signout/$', auth.signout, name='auth_signout'),
    re_path(r'^auth/register/$', auth.register, name='auth_register'),
    re_path(r'^dashboard/$', dashboard.index, name='dashboard'),
    re_path(r'^dashboard/template/(?P<name>[^/]+).html$', dashboard.template),
    re_path(r'^dashboard/views/(?P<name>[^/]+).html$', dashboard.views),

    # SHOULD BE THE LAST IN THIS LIST
    re_path(r'^$', home.index, name='index'),
]
