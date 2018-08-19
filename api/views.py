from logging import getLogger

from django_filters.rest_framework import DjangoFilterBackend
from requests import RequestException
from rest_framework import viewsets, mixins, status, filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.filters import MovieFilter
from api.serializers import MovieSerializer, MovieAddSerializer, MovieAPISerializer, CommentSerializer, \
    transform_search_query_response
from core.models import Movie, Comment
from core.omdbapi import fetch_movie_details

log = getLogger(__name__)


class MovieViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Movie.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = MovieFilter
    ordering_fields = '__all__'

    def get_serializer_class(self):
        if self.action == 'create':
            return MovieAddSerializer
        return MovieSerializer

    def create(self, request, *args, **kwargs):
        input_serializer = MovieAddSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        title = input_serializer.validated_data['title']
        try:
            api_response, not_found = fetch_movie_details(title)
        except RequestException as e:
            log.error(f'Failed when trying to request omdb api. Details: {e}')
            return Response({'detail': 'Occured problem with external system'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not_found:
            return Response({'detail': 'Could not find relevant movie in DB'}, status=status.HTTP_404_NOT_FOUND)

        api_serializer = MovieAPISerializer(data=api_response)
        try:
            api_serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            log.error(f'OMDbAPI replied in unexpected way. Validation error: {e}. Response: {api_response}')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = transform_search_query_response(api_serializer.validated_data)

        override, movie = Movie.should_override(**data)
        if override:
            model_serializer = MovieSerializer(movie, data=data, partial=False)
        else:
            model_serializer = MovieSerializer(data=data)

        try:
            model_serializer.is_valid(raise_exception=True)
        except ValidationError:
            log.error(f'Mapping failed while trying to add a movie to the DB. Data: {data}')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        model_serializer.save()

        headers = self.get_success_headers(input_serializer.data)
        return Response(model_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('movie',)
