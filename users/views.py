from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm 

# Create your views here.
def index(request):
    users = get_user_model().objects.all()
    context = {'users': users,}
    return render(request, 'users/index.html', context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('users:index',)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('users:index')
    else:
        form = CustomUserCreationForm()
    context = {'form': form,}
    return render(request, 'users/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('users:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.Get.get('next') or 'users:index')
    else:
        form = AuthenticationForm()
    context = {'form': form,}
    return render(request, 'users/login.html', context)
    
def logout(request):
    auth_logout(request)
    return redirect('users:index')

def user_detail(request, user_pk):
    auth_user = get_object_or_404(get_user_model(), pk=user_pk)
    ratings = auth_user.rating_set.all()
    movies = auth_user.like_movies.all()
    context = {'auth_user': auth_user, 'ratings': ratings, 'movies': movies,}
    return render(request, 'users/detail.html', context)

@login_required
def follow(request, user_pk):
    person = get_object_or_404(get_user_model(), pk = user_pk)
    user = request.user
    if person != user:
        if person.follow_user.filter(pk=user.pk).exists():
            person.follow_user.remove(user)
        else:
            person.follow_user.add(user)
    return redirect('users:user_detail', person.pk)