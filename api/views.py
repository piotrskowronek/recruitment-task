import requests
from logging import getLogger

from django.utils.text import slugify
from requests import RequestException
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.serializers import MovieSerializer, MovieAddSerializer, MovieAPISerializer
from core.models import Movie

log = getLogger(__name__)


class MovieViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        input_serializer = MovieAddSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        title = input_serializer.validated_data['title']
        try:
            api_response, error = self.fetch_movie_details(title)
        except RequestException as e:
            log.error(f'Failed when trying to request omdb api. Details: {e}')
            return Response({'detail': 'Occured problem with external system'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if error:
            return Response({'detail': 'Could not find relevant movie in DB'}, status=status.HTTP_400_BAD_REQUEST)

        process_serializer = MovieAPISerializer(data=api_response)
        try:
            process_serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            log.error(f'OMDbAPI replied in unexpected way. Validation error: {e}. Response: {api_response}')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = self.transform_search_query_response(process_serializer.validated_data)

        override, movie = Movie.should_override(**data)
        if override:
            output_serializer = MovieSerializer(movie, data=data, partial=False)
        else:
            output_serializer = MovieSerializer(data=data)

        try:
            output_serializer.is_valid(raise_exception=True)
        except ValidationError:
            log.error(f'Mapping failed while trying to add a movie to the DB. Data: {data}')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        output_serializer.save()

        headers = self.get_success_headers(input_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def fetch_movie_details(self, search_query):
        log.info(f'Fetching data from omdbapi. Used search query: {search_query}')
        try:
            response = requests.get(f'http://www.omdbapi.com/?t={search_query}&apikey=b69dd4ec')
        except RequestException as e:
            log.error(f'Encountered an error during fetching data from omdbapi for search query: {search_query}.')
            log.info('Retrying...')
            response = requests.get(f'http://www.omdbapi.com/?t={search_query}&apikey=b69dd4ec')
        json = response.json()
        log.info(f'Fetched data. Response: {json}')

        return json, 'Error' in json

    def transform_search_query_response(self, validated_data):
        mapping = {slugify(k): v for k, v in validated_data.items()}
        return mapping
