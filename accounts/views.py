from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm 
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest

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
            return redirect(request.GET.get('next') or 'accounts:index')
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

    movie_id_list = []
    for rating in ratings:
        tmp = {"title": rating.movie.title, "id": rating.movie_id}
        if tmp not in movie_id_list:
            movie_id_list.append(tmp)
 
    movie_list = list(auth_user.like_movies.all())
    if len(movie_list) > 1:
        movie_first = movie_list.pop(0)
    else:
        movie_first = ''
    context = {'auth_user': auth_user, 'ratings': ratings, 'movies': movie_list, 'movie_id_list': movie_id_list, 'movie_first': movie_first,}
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