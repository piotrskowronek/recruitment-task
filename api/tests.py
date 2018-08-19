from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Movie


class MovieTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        self.client = APIClient()

    def test_empty_list(self):
        """
        Given we have an empty system
        When we request API to list movies
        Then we should have an empty list
        """
        response = self.client.get('/api/movies/')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, [])

    def test_add_simple_movie(self):
        """
        Given we have an empty system
        When we request API to add new movie
        Then we should have added movie
        """
        response = self.client.post('/api/movies/', {'title': 'jackie'})

        self.assertEquals(response.status_code, 201)
        self.assertEquals(Movie.objects.count(), 1)
        movie = Movie.objects.get()
        self.assertEquals(movie.title, 'Jackie')
        self.assertEquals(movie.year, 2016)
        self.assertEquals(movie.imdbid, 'tt1619029')

    def test_add_empty_movie_title(self):
        """
        Given we have an empty system
        When we request API to add new movie without passing movie name
        Then we should have not added movie
        """
        response = self.client.post('/api/movies/', {})

        self.assertEquals(response.status_code, 400)
        self.assertEquals(Movie.objects.count(), 0)

    def test_add_movie_based_on_partial_phrase(self):
        """
        Given we have an empty system
        When we request API to add new movie using only partial part of movie title
        Then we should have added movie
        """
        response = self.client.post('/api/movies/', {'title': 'jac'})

        self.assertEquals(response.status_code, 201)
        self.assertEquals(Movie.objects.count(), 1)
        movie = Movie.objects.get()
        self.assertEquals(movie.title, 'Jac Mac & Rad Boy Go!')
        self.assertEquals(movie.year, 1985)
        self.assertEquals(movie.imdbid, 'tt0875593')

    def test_add_movie_two_times(self):
        """
        Given we have an empty system
        When we request API to add new movie using only partial part of movie title
        Then we should have added movie
        """
        response = self.client.post('/api/movies/', {'title': 'jackie'})
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Movie.objects.count(), 1)

        response = self.client.post('/api/movies/', {'title': 'jackie'})
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Movie.objects.count(), 1)

        response = self.client.post('/api/movies/', {'title': 'jac'})
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Movie.objects.count(), 2)

    def test_add_non_existing_movie(self):
        """
        Given we have an empty system
        When we request API to add new movie which does not exist
        Then we should have empty system
        """
        response = self.client.post('/api/movies/', {'title': 'non existing movie'})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(Movie.objects.count(), 0)
