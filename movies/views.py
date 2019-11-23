from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Movie, Rating
from .forms import RatingForm

# Create your views here.
def movie_list(request):
    movies = Movie.objects.all()
    context = {'movies': movies,}
    return render(request, 'movies/movie_list.html', context)


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.rating_set.all()
    review_form = RatingForm()
    context = {'movie': movie, 'reviews': reviews, 'review_form': review_form,}
    return render(request, 'movies/detail.html', context)


@require_POST
def review_create(request, movie_pk):
    if request.user.is_authenticated:
        review_form = RatingForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie_id = movie_pk
            review.user = request.user
            review.save()
    return redirect('movies:detail', movie_pk)


@require_POST
def review_delete(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if review.user == request.user:
            review.delete()
        return redirect('movies:detail', movie_pk)
    return HttpResponse('You ar Unauthorized', status=401)


@login_required
def like(request, movie_pk):
    if request.is_ajax():
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user
        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            liked = False
        else:
            movie.like_users.add(user)
            liked = True
        
        context = {'liked': liked, 'count': movie.like_users.count()}
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()