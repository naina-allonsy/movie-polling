from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect

from .models import Movie
from django.urls import reverse
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'moviepolls/index.html'
    context_object_name = 'latest_movie_list'

    def get_queryset(self):
        """Return the last five published Movies."""
        return Movie.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Movie
    template_name = 'moviepolls/detail.html'

    def get_queryset(self):
        """
        Excludes any movies that aren't published yet.
        """
        return Movie.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Movie
    template_name = 'moviepolls/results.html'

def vote(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    try:
        selected_choice = movie.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the movie voting form.
        return render(request, 'moviepolls/detail.html', {
            'movie': movie,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('moviepolls:results', args=(movie.id,)))
