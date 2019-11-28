from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from .models import Movie, Rating, Cast, Genre
from .forms import RatingForm
import random

# Create your views here.
def index(request):
    recommend = []
    movies = Movie.objects.all()
    pick = random.choice(movies)

    # 로그인 확인 => user_id 확인
    if request.user.is_authenticated:
        now_user =  get_object_or_404(get_user_model(), pk=request.user.pk)
        ratings = now_user.rating_set.all()

        # user가 남긴 review 가 있는지 확인
        # 평정 5점이 넘고,
        # 있다면 가장 높은 평점을 남긴 영화 genre 첫번째 id를 저장
        if len(ratings) > 0:
            Max_score = -1
            Max_genres = []
            for rating in ratings:
                if Max_score < rating.score and rating.score > 5:
                    Max_score = rating.score
                    Max_genres = rating.movie.title
            
            # # 그 평점에 해당하는 영화들이 3
            # if Max_score_genre != -1:
            #     pass
            # else:
            #     while len(recommend) < 4:
            #         tmp = random.choice(movies)
            #         if tmp not in recommend:
            #             recommend.append(tmp)
        
        context = {'pick': pick, 'recommend': recommend, 'ratings':ratings, 'Max_score':Max_score, 'Max_genres':Max_genres}
        return render(request, 'movies/index.html', context)
        
                
    context = {'pick': pick, 'recommend': recommend}
    return render(request, 'movies/index.html', context)


def movie_list(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    context = {'movies': movies, 'genres': genres}
    return render(request, 'movies/movie_list.html', context)


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.rating_set.all()
    review_form = RatingForm()
    review_update_form = RatingForm()
    casts = movie.cast_set.all()
    
    # # score avg
    # score_list = []
    # for review in reviews:
    #     score_list.append(review.score)
    # score_avg = sum(score_list) / len(reviews)
    context = {'movie': movie, 'reviews': reviews, 'review_form': review_form, 'casts': casts, 'review_update_form': review_update_form,}
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
        review = get_object_or_404(Rating, pk=review_pk)
        if review.user == request.user:
            review.delete()
        return redirect('movies:detail', movie_pk)
    return HttpResponse('You ar Unauthorized', status=401)

@login_required
def review_update(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Rating, pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            review_update_form = RatingForm(request.POST, instance=review)
            if review_update_form.is_valid():
                review = review_update_form.save()
                return redirect('movies:detail', movie_pk)
    return redirect('movies:detail', movie_pk)


def like(request, movie_pk):
    if request.is_ajax():
        movie = get_object_or_404(Movie, pk=movie_pk)
        # user = request.user
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            liked = False
        else:
            movie.like_users.add(request.user)
            liked = True
        
        context = {'liked': liked, 'count': movie.like_users.count(),}
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()