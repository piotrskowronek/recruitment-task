import requests
from django.test import TestCase

from app.settings import OMDB_API_KEY


class OMDbAPITestCase(TestCase):
    """
    Boundary test for OMDbAPI
    Confirms that external API reacts in expected way
    """
    def test_search_single_movie(self):
        """
        Given we have an empty system
        When we request OMDb API to search for a movie with full name
        Then we should have movie details
        """
        response = requests.get(f'http://www.omdbapi.com/?t=jackie&apikey={OMDB_API_KEY}')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['Title'], 'Jackie')
        self.assertEquals(response.json()['Year'], '2016')
        self.assertEquals(response.json()['imdbID'], 'tt1619029')
        self.assertEquals(list(response.json().keys()), ['Title', 'Year','Rated','Released','Runtime','Genre',
                                                         'Director','Writer','Actors','Plot','Language','Country',
                                                         'Awards','Poster','Ratings','Metascore','imdbRating',
                                                         'imdbVotes','imdbID','Type','DVD','BoxOffice','Production',
                                                         'Website','Response'])

    def test_search_based_on_partial_phrase(self):
        """
        Given we have an empty system
        When we request OMDb API to search for a movie with a part of the full name
        Then we should have movie details
        """
        api_key = OMDB_API_KEY
        response = requests.get(f'http://www.omdbapi.com/?t=jac&apikey={OMDB_API_KEY}')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['Title'], 'Jac Mac & Rad Boy Go!')
        self.assertEquals(response.json()['Year'], '1985')
        self.assertEquals(response.json()['imdbID'], 'tt0875593')
        self.assertEquals(list(response.json().keys()), ['Title', 'Year','Rated','Released','Runtime','Genre',
                                                         'Director','Writer','Actors','Plot','Language','Country',
                                                         'Awards','Poster','Ratings','Metascore','imdbRating',
                                                         'imdbVotes','imdbID','Type','DVD','BoxOffice','Production',
                                                         'Website','Response'])

    def test_search_based_on_wider_phrase(self):
        """
        Given we have an empty system
        When we request OMDb API to search for a movie with a wider name than existing
        Then we should have movie details
        """
        response = requests.get(f'http://www.omdbapi.com/?t=jackie+brown&apikey={OMDB_API_KEY}')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['Title'], 'Jackie Brown')
        self.assertEquals(response.json()['Year'], '1997')
        self.assertEquals(response.json()['imdbID'], 'tt0119396')
        self.assertEquals(list(response.json().keys()), ['Title', 'Year','Rated','Released','Runtime','Genre',
                                                         'Director','Writer','Actors','Plot','Language','Country',
                                                         'Awards','Poster','Ratings','Metascore','imdbRating',
                                                         'imdbVotes','imdbID','Type','DVD','BoxOffice','Production',
                                                         'Website','Response'])

    def test_two_movies_with_identical_name(self):
        """
        Given we have an empty system
        When we request OMDb API to search for a movie title which occurs multiple times
        Then we should have movie details, every time the same
        """
        for _ in range(3):
            response = requests.get(f'http://www.omdbapi.com/?t=les+misérables&apikey={OMDB_API_KEY}')

            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.json()['Title'], 'Les Misérables')
            self.assertEquals(response.json()['Year'], '2012')
            self.assertEquals(response.json()['imdbID'], 'tt1707386')
            self.assertEquals(list(response.json().keys()), ['Title', 'Year','Rated','Released','Runtime','Genre',
                                                             'Director','Writer','Actors','Plot','Language','Country',
                                                             'Awards','Poster','Ratings','Metascore','imdbRating',
                                                             'imdbVotes','imdbID','Type','DVD','BoxOffice','Production',
                                                             'Website','Response'])

    def test_non_existing_movie(self):
        """
        Given we have an empty system
        When we request OMDb API to search for a movie which does not exist
        Then we should have error response
        """
        response = requests.get(f'http://www.omdbapi.com/?t=non+existing+movie&apikey={OMDB_API_KEY}')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'Response': 'False', 'Error': 'Movie not found!'})