from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    userid = models.OneToOneField(User,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50)
    dob = models.DateField(null=True)
    mob = models.CharField(max_length=10)

class Theatre(models.Model):
    theatre_name = models.CharField(max_length=50)
    city = models.CharField(max_length=20)

    def __str__(self):
        return self.theatre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=25)
    show_time = models.TimeField()
    show = models.ForeignKey(Theatre, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        abc = ['A', 'B', 'C', 'D', 'E', 'F']
        for j in range(6):
            for i in range(15):
                s = Seat(seat_id=abc[j] + str(i+1), cost=100, movie=self, show=self.show)
                s.save()


class Seat(models.Model):
    seat_id = models.CharField(max_length=4)
    seat_state = models.BooleanField(default=False)
    cost = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show = models.ForeignKey(Theatre, on_delete=models.CASCADE)

class Tickets(models.Model):
    ticket_id = models.CharField(max_length=75)
    username = models.CharField(max_length=20)
    seat = models.ForeignKey(Seat, on_delete = models.CASCADE)
