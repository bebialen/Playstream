from django.shortcuts import render,get_object_or_404,redirect
from .models import Genre,Movie,Season,Series,Episode,WatchlistItem,Watchlist2, RecentMovie, RecentEpisode,MovieReview
from .forms import UserRegistrationForm,ContentCreatorRegistrationForm,CustomLoginForm,MovieForm,SeasonForm,SeriesForm,EpisodeForm,UserProfileForm
from .forms import UserEditForm, UserProfileForm, UserProfile ,MovieReviewForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect



# Create your views here.


from django.shortcuts import render
from .models import Movie, Genre  # Import the Movie and Genre models as needed

def HomePage(request):
    return render(request,'homepage.html')


def AboutUs(request):
    return render(request,'about_us.html')

def Admin(request):
    return render(request,'admin.html')



def mycontents(request):
    if request.user.is_authenticated:
        # User is authenticated, so show their content
        movies = Movie.objects.filter(post_author=request.user)
        series = Series.objects.filter(post_author=request.user)
    else:
        # User is not authenticated, so do not show any content
        movies = []
        series = []

    return render(request, 'my_contents.html', {'movies': movies, 'series': series})


def view1(request):
    # Get the search term posted from the form with name 'searchpost'
    search_term = request.GET.get('searchpost')

    # Initialize genres_with_movies as an empty list
    genres_with_movies = []

    # Initialize movie_details as an empty list
    movie_details = []

    if search_term:
        # Filter movies by name if a search term is provided
        movie_details = Movie.objects.filter(title__icontains=search_term)
    else:
        # Retrieve all genres and their associated movies
        genres = Genre.objects.filter(is_disabled=False)

        for genre in genres:
            movies = Movie.objects.filter(genre=genre,is_disabled=False)
            genres_with_movies.append({
                'genre': genre,
                'movies': movies,
            })

    return render(request, "moviepage.html", {
        'search_term': search_term,
        'genres_with_movies': genres_with_movies,
        'movie_details': movie_details,
    })

def view_movie(request, passed_id):
    #Getting the get method var and passing that along with the model
    view_movies = get_object_or_404(Movie, id=passed_id)
    movies_with_same_genre = Movie.objects.filter(genre=view_movies.genre).exclude(id=passed_id)
    return render(request,"view_movie.html",{'view_movies':view_movies,'movies_with_same_genre': movies_with_same_genre})

def series_list(request):
    # Get the search term posted from the form with name 'searchpost'
    search_term = request.GET.get('searchpost')

    # Initialize genres_with_series as an empty list
    genres_with_series = []

    # Initialize series_details as an empty list
    series_details = []

    if search_term:
        # Filter series by name if a search term is provided
        series_details = Series.objects.filter(title__icontains=search_term)
    else:
        # Retrieve all genres and their associated series
        genres = Genre.objects.filter(is_disabled=False)

        for genre in genres:
            series = Series.objects.filter(genre=genre,is_disabled=False)
            genres_with_series.append({
                'genre': genre,
                'series': series,
            })

    return render(request, "seriespage.html", {
        'search_term': search_term,
        'genres_with_series': genres_with_series,
        'series_details': series_details,
    })

def view_series(request, passed_id):
    # Getting the get method var and passing that along with the model
    view_series = get_object_or_404(Series, id=passed_id)
    seasons = Season.objects.filter(series=view_series,is_disabled=False)
    episodes = Episode.objects.filter(season__in=seasons,is_disabled=False)
    series_with_same_genre = Series.objects.filter(genre=view_series.genre).exclude(id=passed_id)
    return render(request, "view_series.html", {'view_series': view_series, 'seasons': seasons, 'episodes': episodes,'series_with_same_genre':series_with_same_genre})



def register(request):
    if request.method == 'POST': #Will get the posted variablesm from the MyLoginForm
        user_reg_form = UserRegistrationForm(request.POST) #checking if the post request parameters are valid
        if user_reg_form.is_valid():
            #Receive the data,create the form,do not save it ,just keep it
            new_user = user_reg_form.save(commit=False)
            #set the password with the cleaned data for password
            #cleaned dta will automatically e calling be  calling the form's clean_passwod2 function
            new_user.set_password(user_reg_form.cleaned_data['password'])
            # permanently save the new user model data into the database
            new_user.save()
            return render(request,'account/user_register_done.html',{'user_reg_form':user_reg_form})
    else: #if the user registration form is not valid or not submitted
        #in that case give the user ,the blank registration form from register.html

        user_reg_form = UserRegistrationForm()
        #if the user is not submitting the form,render the registration form.
    return render(request,'account/user_register.html',{'user_reg_form':user_reg_form})







def register_content(request):
    if request.method == 'POST': #Will get the posted variablesm from the MyLoginForm
        review_reg_form = ContentCreatorRegistrationForm(request.POST) #checking if the post request parameters are valid
        if review_reg_form.is_valid():
            #Receive the data,create the form,do not save it ,just keep it
            new_user = review_reg_form.save(commit=False)
            #set the password with the cleaned data for password
            #cleaned dta will automatically e calling be  calling the form's clean_passwod2 function
            new_user.set_password(review_reg_form.cleaned_data['password'])
            # permanently save the new user model data into the database
            new_user.save()
            #add the user by default to the reviewers group
            reviewers_group = Group.objects.get(name='contents')
            new_user.groups.add(reviewers_group)
            return render(request,'account/user_register_done.html',{'review_reg_form':review_reg_form})
    else: #if the user registration form is not valid or not submitted
        #in that case give the user ,the blank registration form from register.html

        review_reg_form = ContentCreatorRegistrationForm()
        #if the user is not submitting the form,render the registration form.
    return render(request,'account/content_register.html',{'review_reg_form':review_reg_form})



class CustomLoginView(LoginView):
    template_name = 'custom_login.html'  # Specify your custom login template
    authentication_form = CustomLoginForm  # Use your custom form

    def form_valid(self, form):

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")

        # Redirect back to the login page (or any other page you prefer).
        return super().form_invalid(form)


def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the post_author field to the currently authenticated user
            form.instance.post_author = request.user
            form.save()
            # Redirect to a success page or do something else
            return redirect('my_contents')
    else:
        form = MovieForm()
    return render(request, 'add/add_movie.html', {'movie_form': form})


def create_series(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the post_author field to the currently authenticated user
            series = form.save(commit=False)
            series.post_author = request.user
            series.save()
            # Redirect to the next step, passing series id in the URL
            return redirect('create_season',series_id = series.id)
    else:
        form = SeriesForm()
    return render(request, 'add/add_series.html', {'series_form': form})

def create_season(request, series_id):
    series = Series.objects.get(id=series_id)
    if request.method == 'POST':
        form = SeasonForm(request.POST)
        if form.is_valid():
            season = form.save(commit=False)
            season.series = series
            season.save()
            # Redirect to the next step, passing season id in the URL
            return redirect('create_episode', series_id=series.id, season_id=season.id)

    else:
        form = SeasonForm()
    return render(request, 'add/add_season.html', {'season_form': form})

def create_episode(request, series_id, season_id):
    season = Season.objects.get(id=season_id)
    if request.method == 'POST':
        form = EpisodeForm(request.POST)
        if form.is_valid():
            episode = form.save(commit=False)
            episode.season = season
            episode.save()
            # Redirect to a success page or do something else
            return redirect('my_contents')
    else:
        form = EpisodeForm()
    return render(request, 'add/add_episode.html', {'episode_form': form})

def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            view_movie_url = reverse('view_movie', args=[movie.id])
            return redirect(view_movie_url)

    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit/edit_movie.html', {'edit_movie_form': form, 'movie': movie})

def edit_series(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    if request.method == 'POST':
        form = SeriesForm(request.POST, request.FILES, instance=series)
        if form.is_valid():
            form.save()
            # Redirect to a success page or series details page
            next_step_url = reverse('view_series', args=[series.id])
            return redirect(next_step_url)
    else:
        form = SeriesForm(instance=series)
    return render(request, 'edit/edit_series.html', {'edit_series_form': form, 'series': series})

def edit_season(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    if request.method == 'POST':
        form = SeasonForm(request.POST, instance=season)
        if form.is_valid():
            form.save()
            # Redirect to a success page or season details page
            season_details_url = reverse('view_series', args=[season.series.id])
            return redirect(season_details_url)
    else:
        form = SeasonForm(instance=season)
    return render(request, 'edit/edit_season.html', {'edit_season_form': form, 'season': season})

def edit_episode(request, episode_id):
    episode = get_object_or_404(Episode, id=episode_id)
    if request.method == 'POST':
        form = EpisodeForm(request.POST, instance=episode)
        if form.is_valid():
            form.save()
            # Redirect to a success page or episode details page
            view_series_url = reverse('view_series', args=[episode.season.series.id])
            return redirect(view_series_url)
    else:
        form = EpisodeForm(instance=episode)
    return render(request, 'edit/edit_episode.html', {'edit_episode_form': form, 'episode': episode})

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    # Redirect to a success page or movie list page
    return redirect('my_contents')

# Delete Series
def delete_series(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    series.delete()
    # Redirect to a success page or series list page
    return redirect('my_contents')

# Delete Season
def delete_season(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    season.delete()
    # Redirect to a success page or series details page (or wherever appropriate)
    return redirect('view_series', passed_id=season.series.id)

# Delete Episode
def delete_episode(request, episode_id):
    episode = get_object_or_404(Episode, id=episode_id)
    episode.delete()
    # Redirect to a success page or season details page (or wherever appropriate)
    return redirect('view_series', passed_id=episode.season.series.id)



def add_to_watchlist(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=movie_id)
        # Check if a watchlist item for the same user and movie already exists
        existing_watchlist_item = WatchlistItem.objects.filter(user=request.user, movie=movie).first()
        if not existing_watchlist_item:
            watchlist_item = WatchlistItem(user=request.user, movie=movie)
            watchlist_item.save()
    return redirect('movie')


def add_series_to_watchlist(request, series_id):
    if request.user.is_authenticated:
        series = get_object_or_404(Series, id=series_id)
        # Check if a watchlist item for the same user and series already exists
        existing_watchlist_item = Watchlist2.objects.filter(user=request.user, series=series).first()
        if not existing_watchlist_item:
            watchlist_item = Watchlist2(user=request.user, series=series)
            watchlist_item.save()
    return redirect('series_list')

def remove_from_watchlist(request, watchlist_item_id):
    if request.user.is_authenticated:
        watchlist_item = get_object_or_404(WatchlistItem, id=watchlist_item_id, user=request.user)
        watchlist_item.delete()
    # Redirect back to the watchlist page
    return redirect('watchlist')

def remove_series_from_watchlist(request, watchlist_item_id):
    if request.user.is_authenticated:
        watchlist_item = get_object_or_404(Watchlist2, id=watchlist_item_id, user=request.user)
        watchlist_item.delete()
    # Redirect back to the watchlist2 page
    return redirect('watchlist')


def watchlist(request):
    if request.user.is_authenticated:
        watchlist_items = WatchlistItem.objects.filter(user=request.user)
        watchlist_items2 = Watchlist2.objects.filter(user=request.user)
        return render(request, 'watchlist.html', {'watchlist_items': watchlist_items, 'watchlist_items2': watchlist_items2})
    else:
        return redirect('login')



def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('edit_profile')  # Redirect to the profile edit page after successful form submission
    else:
        user_form = UserEditForm(instance=request.user)  # Initialize user form without initial data
        profile_form = UserProfileForm(instance=user_profile)  # Initialize profile form without initial data

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})




def add_to_recent_movie(request, movie_id):
    # Get the Movie instance
    movie = get_object_or_404(Movie, id=movie_id)

    # Assuming you have the current user available in request.user
    user = request.user

    # Create a RecentMovie instance with the watched_movie field set to the movie instance
    RecentMovie.objects.create(user=user, watched_movie=movie)

    # Redirect to a success page or back to the movie details page
    return HttpResponseRedirect(reverse('view_movie', args=[movie_id]))

def episode_detail(request, episode_id):
    episode = get_object_or_404(Episode, id=episode_id)
    context = {
        'episode': episode,
    }
    return render(request, 'episode_detail.html', context)

def add_to_recent_episode(request, episode_id):
    episode = get_object_or_404(Episode, id=episode_id)

    user = request.user
    # Create a RecentEpisode instance with the watched_episode field set to the episode instance
    RecentEpisode.objects.create(user=user, watched_episode=episode)

    # Redirect to a success page or back to the episode details page
    return HttpResponseRedirect(reverse('view_series', args=[episode_id]))

def recent_movies(request):
    recent_movies = RecentMovie.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, 'recent_movies.html', {'recent_movies': recent_movies})

def recent_episodes(request):
    recent_episodes = RecentEpisode.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, 'recent_episode.html', {'recent_episodes': recent_episodes})


def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            # Redirect to the movie detail page or any other appropriate page
            return redirect('view_movie', movie_id=movie.id)
    else:
        form = MovieReviewForm()

    return render(request, 'review/add_movie_review.html', {'form': form, 'movie': movie})


def edit_review(request, movie_id):
    # Get the Movie instance
    movie = get_object_or_404(Movie, id=movie_id)

    # Get the review associated with the movie and the currently logged-in user
    review = get_object_or_404(MovieReview, user=request.user, movie=movie)

    if request.method == 'POST':
        form = MovieReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            # Redirect to the movie detail page after the review is successfully edited
            return redirect('view_movie', movie_id=movie.id)
    else:
        form = MovieReviewForm(instance=review)

    return render(request, 'review/edit_movie_review.html', {'form': form, 'movie': movie})


def delete_review(request, movie_id):
    # Get the Movie instance
    movie = get_object_or_404(Movie, id=movie_id)

    # Get the review associated with the movie and the currently logged-in user
    review = get_object_or_404(MovieReview, user=request.user, movie=movie)

    # Delete the review
    review.delete()

    # Redirect to the movie detail page after the review is successfully deleted
    return redirect('view_movie', movie_id=movie.id)


def view_reviews(request, movie_id):
    # Get the Movie instance
    movie = get_object_or_404(Movie, id=movie_id)

    # Get the user's review for the movie
    user_review = MovieReview.objects.filter(user=request.user, movie=movie).first()

    # Get all reviews for the movie
    all_reviews = MovieReview.objects.filter(movie=movie)

    return render(request, 'review/movie_review.html',
                  {'movie': movie, 'user_review': user_review, 'all_reviews': all_reviews, 'view_movies': movie})