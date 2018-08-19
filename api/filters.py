from django_filters import rest_framework as filters

from core.models import Movie


class MovieFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    year_from = filters.NumberFilter(field_name="year", lookup_expr='gte')
    year_to = filters.NumberFilter(field_name="year", lookup_expr='lte')

    class Meta:
        model = Movie
        fields = ['title', 'year_from', 'year_to']