from django.conf.urls import url
from django.conf.urls import url
from home.views import *
from .views import *

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^adduser/$', adduser, name="adduser"),
    url(r'^signup/$', signup),
    url(r'^signedup/$', signedup),
    url(r'^auth/$', auth_view),
    url(r'^logout/$', logout),
    url(r'^loggedin/$', loggedin),
    url(r'^invalidlogin/$', invalidlogin),
    url(r'^index/$', index, name="home"),
    url(r'^profileupdate/$', profileupdate),
    url(r'^profileupdate/login/update/$', update),
    url(r'^$', login),

]
