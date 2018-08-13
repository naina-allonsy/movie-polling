from django.contrib import admin

# Register your models here.
from .models import Movie, Choice

class MovieAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['movie_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    list_display = ('movie_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['movie_text']

admin.site.register(Movie, MovieAdmin)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
