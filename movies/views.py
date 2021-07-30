from django.shortcuts import render
from .models import Movie

# Create your views here.
def index(request):
    new_releases = Movie.objects.order_by('-created_at')[:5]
    films = Movie.objects.filter(movie_type='fi')
    series = Movie.objects.filter(movie_type='se')
    cartouns = Movie.objects.filter(movie_type='ca')
    context = {
        'films': films,
        'series': series,
        'cartoons': cartouns,
        'new_releases': new_releases,
    }
    return render(request, "movies/index.html", context)

def detail_view(request, pk):
    movie = Movie.objects.get(id=pk)
    return render(request, 'movies/movie-detail.html', context={'movie': movie})
