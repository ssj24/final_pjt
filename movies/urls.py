from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.movie_list, name='list'),
    path('list/<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/review/', views.review_create, name='review_create'),
    path('<int:movie_pk>/review/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:movie_pk>/review/<int:review_pk>/update/', views.review_update, name='review_update'),
]