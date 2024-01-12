from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

# Signal to create UserProfile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Signal to save UserProfile when User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()






# Create a Genre model for movies and series
class Genre(models.Model):
    name = models.CharField(max_length=100)
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Model for Movies
class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='post/images', blank=True)
    youtube_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)  # Default to the first user (you can customize this)
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Model for TV Series
class Series(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    poster_image = models.ImageField(upload_to='series/posters/', blank=True)  # Field for storing the poster image
    youtube_link = models.URLField(blank=True)  # Field to store the YouTube link
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)  # Default to the first user (you can customize this)
    is_disabled = models.BooleanField(default=False)


    def __str__(self):
        return self.title

# Model for Series Seasons
class Season(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    season_number = models.PositiveIntegerField()
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.series.title} - Season {self.season_number}"


# Model for Series Episodes
class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    youtube_link = models.URLField(blank=True)
    is_disabled = models.BooleanField(default=False)# Field to store the YouTube link for the episode

    def __str__(self):
        return f"{self.season.series.title} - Season {self.season.season_number}, Episode {self.episode_number}: {self.title}"



class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')


class Watchlist2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'series')

    def __str__(self):
        return f"Watchlist2 Item for {self.user.username}"



class RecentMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watched_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recent watch: Movie - {self.watched_movie.title} by {self.user.username}"


class RecentEpisode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watched_episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recent watch: Episode - {self.watched_episode.title} by {self.user.username}"


class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)  # Assuming you have a Movie model
    rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 11)])  # Allowing ratings from 1 to 10
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.movie.title}"