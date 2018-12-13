from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import TheatreForm
from .models import *
from django.contrib.auth.decorators import login_required
import random
import string
from django.template.context_processors import csrf


def index(request):
    return render(request, 'base_visitor.html')


@login_required
def add_theatre(request):
    form = TheatreForm(request.POST)
    if form.is_valid():
        theatre = form.save(commit=False)
        form = TheatreForm()
        context = {
            "theatre": theatre.theatre_name,
            "form": form
        }
        theatre.save()
        return render(request, "addtheatre.html", context)
    context = {
        "form": form,
    }
    return render(request, 'addtheatre.html', context)


@login_required
def search_theatre(request):
    search = request.GET.get('search', '')
    theatres = Theatre.objects.filter(city__startswith=search)
    return render(request, 'base_visitor.html', {'theatres': theatres})


@login_required
def search_movie(request):
    searchm = request.GET.get('searchm')
    city = Theatre.objects.filter(city__iregex=searchm)
    for c in city:
        city = c.city
        break
    if not city:
        return render(request, 'home.html', {'city': True})
    else:
        movies = Movie.objects.filter(show__city__startswith=city).values_list('movie_name', flat=True).distinct()
        movies = movies.order_by('movie_name')
        return render(request, 'base_visitor.html', {'movies': movies, 'city': city, 'search': True})


@login_required
def movie_select(request, city, movie_name):
    movie = Movie.objects.filter(movie_name=movie_name, show__city__startswith=city)
    movie = movie.order_by('show_time')
    return render(request, 'base_visitor.html', {'movie': movie, 'city1': city, 'movie_name': movie_name})


@login_required
def seat_select(request, show):
    seats = Seat.objects.filter(movie=show)
    request.session['show'] = show
    return render(request, 'base_visitor.html', {'seats': seats})


@login_required
def book(request):
    if 'show' in request.session:
        show = request.session['show']
    seats = request.POST.get('seatsSelected')
    # print(seats)
    seats = seats.split(",")
    request.session['seats'] = seats
    movie = Movie.objects.get(id=show)
    cost = 0.00
    for s in seats:
        c = Seat.objects.get(seat_id=s, movie=show)
        cost = cost + c.cost
    return render(request, 'base_visitor.html', {'cost2': cost})


@login_required
def update_seats(request):
    if 'seats' in request.session:
        seats = request.session['seats']
    if 'show' in request.session:
        show = request.session['show']
    ticket_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    for s in seats:
        print(s)
        seat = Seat.objects.get(seat_id=s, movie=show)
        if not seat.seat_state:
            seat.seat_state = True
        else:
            return HttpResponseRedirect('/home/' + show + '?isselected=1')
        seat.save()
        t1 = Tickets(ticket_id=ticket_id, seat=seat, username=request.user.username)
        t1.save()
    # request.session['tick_id'] = ticket_id
    return HttpResponseRedirect('/home/ticket/')


@login_required
def ticket(request):
    show = request.session['show']
    seats = request.session['seats']
    movie = Movie.objects.get(id=show)
    cost = 0.00
    for s in seats:
        c = Seat.objects.get(seat_id=s, movie=show)
        cost = cost + c.cost
    return render(request, 'base_visitor.html', {'book': seats, 'movie_book': movie, 'cost': cost})


@login_required
def home_page(request):
    return render(request, 'home.html', {'city': False})


@login_required
def ticket_update(request, t_id):
    # print(t_id)
    c = {}
    c.update(csrf(request))
    t = Tickets.objects.filter(username=request.user.username)
    c.update({"t": t})
    s = Tickets.objects.filter(ticket_id=t_id)
    for ss in s:
        ss.seat.seat_state = False
        ss.seat.save()
        ss.delete()
    c.update({'ticket_up': True})
    return render(request, 'tickets_show.html', c)


