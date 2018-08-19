from rest_framework import serializers

from core.models import Movie


class MovieAddSerializer(serializers.Serializer):
    title = serializers.CharField()


class MovieAPISerializer(serializers.Serializer):
    Title = serializers.CharField()
    Year = serializers.CharField()
    Rated = serializers.CharField()
    Released = serializers.CharField()
    Runtime = serializers.CharField()
    Genre = serializers.CharField()
    Director = serializers.CharField()
    Writer = serializers.CharField()
    Actors = serializers.CharField()
    Plot = serializers.CharField()
    Language = serializers.CharField()
    Country = serializers.CharField()
    Awards = serializers.CharField()
    Poster = serializers.CharField()
    Ratings = serializers.JSONField()
    Metascore = serializers.CharField()
    imdbRating = serializers.CharField()
    imdbVotes = serializers.CharField()
    imdbID = serializers.CharField()
    Type = serializers.CharField()
    DVD = serializers.CharField()
    BoxOffice = serializers.CharField()
    Production = serializers.CharField()
    Website = serializers.CharField()
    Response = serializers.CharField()

    class Meta:
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
