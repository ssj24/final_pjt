from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm 
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
import random

# Create your views here.
def index(request):
    if request.user.is_staff:
        users = get_user_model().objects.all()
        context = {'users': users,}
        return render(request, 'accounts/index.html', context)
    else:
        return redirect('movies:index')

def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:index',)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {'form': form,}
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {'form': form,}
    return render(request, 'accounts/login.html', context)
    
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')


@require_POST
def delete(request):
    request.user.delete()
    return redirect('movies:list')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)



def user_detail(request, user_pk):
    auth_user = get_object_or_404(get_user_model(), pk=user_pk)
    ratings = auth_user.rating_set.all()
    movies = auth_user.like_movies.all()
    if auth_user.following_user.all():
        followings = auth_user.following_user.all()
        randomf = random.choice(followings)
        if randomf.like_movies.all():
            randomms = randomf.like_movies.all()
            randomm = random.choice(randomms)
        else: randomm = ''
    else:
        randomf = ''
        randomm = ''
    context = {'auth_user': auth_user, 'ratings': ratings, 'movies': movies, 'randomf': randomf, 'randomm': randomm}
    return render(request, 'accounts/detail.html', context)

@login_required
def follow(request, user_pk):
    person = get_object_or_404(get_user_model(), pk = user_pk)
    user = request.user
    if request.is_ajax():
        if person != user:
            if person.follow_user.filter(pk=user.pk).exists():
                person.follow_user.remove(user)
                followed = False
            else:
                person.follow_user.add(user)
                followed = True
        context = {'followed': followed, 'count': person.follow_user.count(),}
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest