from django.contrib import admin
from django.urls import path
from .views import view1,HomePage,view_movie,series_list,view_series,register,register_content,mycontents,add_to_watchlist,watchlist,remove_from_watchlist,add_series_to_watchlist,remove_series_from_watchlist,Admin,add_review,view_reviews,edit_review,delete_review
from .views import create_movie,create_season,create_episode,create_series,edit_movie,edit_season,edit_episode,edit_series,delete_movie,delete_season,delete_episode,delete_series,AboutUs,edit_profile,add_to_recent_episode,episode_detail,recent_movies,recent_episodes,add_to_recent_movie
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView

urlpatterns = [
    path('',HomePage,name='home'),
    path('movie/',view1,name='movie'),
    path('about_us/', AboutUs, name='about_us'),

    path('admin/', Admin, name='admin'),

    path('my_contents/', mycontents, name='my_contents'),
    path('view_movie/<int:passed_id>/', view_movie, name='view_movie'),
    path('view_movie/<int:movie_id>/', view_movie, name='view_movie'),

    path('view_series/<int:passed_id>/', view_series, name='view_series'),
    path('view_series/<int:series_id>/', view_series, name='view_series'),

    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('series/', series_list, name='series_list'),
    path('accounts/register/', register, name='register'),
    path('accounts/register_content/',register_content , name='register_content'),


    path('create/movie/', create_movie, name='create_movie'),
    path('create/series/', create_series, name='create_series'),
    path('create/season/<int:series_id>/', create_season, name='create_season'),
    path('create/episode/<int:series_id>/<int:season_id>/', create_episode, name='create_episode'),



    path('edit/movie/<int:movie_id>/', edit_movie, name='edit_movie'),
    path('edit/series/<int:series_id>/', edit_series, name='edit_series'),
    path('edit/season/<int:season_id>/', edit_season, name='edit_season'),
    path('edit/episode/<int:episode_id>/', edit_episode, name='edit_episode'),

    path('delete/movie/<int:movie_id>/', delete_movie, name='delete_movie'),
    path('delete/series/<int:series_id>/', delete_series, name='delete_series'),
    path('delete/season/<int:season_id>/', delete_season, name='delete_season'),
    path('delete/episode/<int:episode_id>/', delete_episode, name='delete_episode'),


    path('add_to_watchlist/<int:movie_id>/', add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', watchlist, name='watchlist'),
    path('remove_from_watchlist/<int:watchlist_item_id>/', remove_from_watchlist, name='remove_from_watchlist'),
    path('add_series_to_watchlist/<int:series_id>/', add_series_to_watchlist, name='add_series_to_watchlist'),
    path('remove_series_from_watchlist/<int:watchlist_item_id>/', remove_series_from_watchlist,
         name='remove_series_from_watchlist'),

    path('profile/', edit_profile, name='edit_profile'),

path('add_to_recent_episode/<int:episode_id>/', add_to_recent_episode, name='add_to_recent_episode'),
    path('episodes/<int:episode_id>/', episode_detail, name='episode_detail'),

    path('movie/recent_movies/', recent_movies, name='recent_movies'),
    path('series/recent_episode/', recent_episodes, name='recent_episodes'),
path('recent_watchlist/<int:movie_id>/', add_to_recent_movie, name='add_to_recent_watchlist'),

    path('accounts/password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change/done', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('movies/add_review/<int:movie_id>/', add_review, name='add_review'),
    path('movie/reviews/<int:movie_id>', view_reviews, name='view_reviews'),
    path('movie/edit_review/<int:movie_id>', edit_review, name='edit_review'),
    path('movie/delete_review/<int:movie_id>', delete_review, name='delete_review'),
]
