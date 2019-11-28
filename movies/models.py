from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    
class Movie(models.Model):
    title = models.CharField(max_length=150)
    audience = models.IntegerField()
    start_date = models.CharField(max_length=50)
    director = models.CharField(max_length=45)
    poster_url = models.CharField(max_length=150)
    summary = models.TextField() 
    genres = models.ManyToManyField(Genre, related_name='movie_genres', blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)
    teaser = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    character = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    profile_path = models.CharField(max_length=50, blank=True)


class Rating(models.Model):
    comment = models.TextField()
    score = models.PositiveIntegerField(default=10, validators=[MaxValueValidator(10), MinValueValidator(0)])
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment