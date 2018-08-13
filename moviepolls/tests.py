import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Movie


class MovieModelTests(TestCase):

    def test_was_published_recently_with_future_movie(self):
        """
        was_published_recently() returns False for movies whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_movie = Movie(pub_date=time)
        self.assertIs(future_movie.was_published_recently(), False)

    def test_was_published_recently_with_old_movie(self):
        """
        was_published_recently() returns False for movies whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_movie = Movie(pub_date=time)
        self.assertIs(old_movie.was_published_recently(), False)

    def test_was_published_recently_with_recent_movie(self):
        """
        was_published_recently() returns True for movies whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_movie = Movie(pub_date=time)
        self.assertIs(recent_movie.was_published_recently(), True)

def create_movie(movie_text, days):
    """
    Create a movie with the given `movie_text` and published the
    given number of `days` offset to now (negative for movies published
    in the past, positive for movies that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Movie.objects.create(movie_text=movie_text, pub_date=time)


class MovieIndexViewTests(TestCase):
    def test_no_movies(self):
        """
        If no movies exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('moviepolls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_movie_list'], [])

    def test_past_movie(self):
        """
        Movies with a pub_date in the past are displayed on the
        index page.
        """
        create_movie(movie_text="Past movie.", days=-30)
        response = self.client.get(reverse('moviepolls:index'))
        self.assertQuerysetEqual(
            response.context['latest_movie_list'],
            ['<Movie: Past movie.>']
        )

    def test_future_movie(self):
        """
        Movies with a pub_date in the future aren't displayed on
        the index page.
        """
        create_movie(movie_text="Future movie.", days=30)
        response = self.client.get(reverse('moviepolls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_movie_list'], [])

    def test_future_movie_and_past_movie(self):
        """
        Even if both past and future movies exist, only past movies
        are displayed.
        """
        create_movie(movie_text="Past movie.", days=-30)
        create_movie(movie_text="Future movie.", days=30)
        response = self.client.get(reverse('moviepolls:index'))
        self.assertQuerysetEqual(
            response.context['latest_movie_list'],
            ['<Movie: Past movie.>']
        )

    def test_two_past_movies(self):
        """
        The movies index page may display multiple movies.
        """
        create_movie(movie_text="Past movie 1.", days=-30)
        create_movie(movie_text="Past movie 2.", days=-5)
        response = self.client.get(reverse('moviepolls:index'))
        self.assertQuerysetEqual(
            response.context['latest_movie_list'],
            ['<Movie: Past movie 2.>', '<Movie: Past movie 1.>']
        )

class MovieDetailViewTests(TestCase):
    def test_future_movie(self):
        """
        The detail view of a movie with a pub_date in the future
        returns a 404 not found.
        """
        future_movie = create_movie(movie_text='Future movie.', days=5)
        url = reverse('moviepolls:detail', args=(future_movie.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_movie(self):
        """
        The detail view of a movie with a pub_date in the past
        displays the movie's text.
        """
        past_movie = create_movie(movie_text='Past movie.', days=-5)
        url = reverse('moviepolls:detail', args=(past_movie.id,))
        response = self.client.get(url)
        self.assertContains(response, past_movie.movie_text)
