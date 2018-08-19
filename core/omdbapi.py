from logging import getLogger

import requests
from requests import RequestException

from app.settings import OMDB_API_KEY

log = getLogger(__name__)


def fetch_movie_details(search_query):
    log.info(f'Fetching data from omdbapi. Used search query: {search_query}')
    try:
        response = requests.get(f'http://www.omdbapi.com/?t={search_query}&apikey={OMDB_API_KEY}')
    except RequestException as e:
        log.error(f'Encountered error during fetching data from omdbapi for search query: {search_query}. Details: {e}')
        log.info('Retrying...')
        response = requests.get(f'http://www.omdbapi.com/?t={search_query}&apikey={OMDB_API_KEY}')
    json = response.json()
    log.info(f'Fetched data. Response: {json}')

    return json, 'Error' in json