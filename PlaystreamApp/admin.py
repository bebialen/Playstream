from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Genre, Movie, Series, Season, Episode

# Custom admin actions
def disable_selected(modeladmin, request, queryset):
    queryset.update(is_disabled=True)

def enable_selected(modeladmin, request, queryset):
    queryset.update(is_disabled=False)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_disabled')
    actions = [disable_selected, enable_selected]

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'is_disabled')
    actions = [disable_selected, enable_selected]

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'is_disabled')
    actions = [disable_selected, enable_selected]

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'season_number', 'is_disabled')
    actions = [disable_selected, enable_selected]

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'episode_number', 'title', 'is_disabled')
    actions = [disable_selected, enable_selected]
