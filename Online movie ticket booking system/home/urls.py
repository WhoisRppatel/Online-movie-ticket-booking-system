from django.urls import path
from django.conf.urls import url
from . import views
from login import views as v

urlpatterns = [
    url(r'^ticket/$',views.ticket,name='ticket_view'),
    url(r'^book/$', views.book, name='book'),
    url(r'^update_seats/$', views.update_seats, name='update_seats'),
    path('', views.index, name='index'),
    url(r'^home_page/$', views.home_page, name='home_page'),
    url(r'^profile/$', v.profile, name='profile'),
    url(r'^tickets/$', v.tickets, name='tickets'),
    url(r'^logout/$', v.logout, name='logout'),
    url(r'^login/$', v.login, name='login'),
    url(r'^add_theatre/$', views.add_theatre, name='add_theatre'),
    url(r'^search_theatre/$', views.search_theatre, name="search_theatre"),
    url(r'^search_movie/$', views.search_movie, name="search_movie"),
    url(r'^(?P<city>[\w ]+)[/](?P<movie_name>[\w ]*)$', views.movie_select, name='bymovie'),
    url(r'^(?P<show>[\d ]*)$', views.seat_select, name='seat'),
    url(r'^tickets/delete/(?P<t_id>[\w]+)$',views.ticket_update,name="ticket_update")

]
