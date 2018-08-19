from django.contrib.postgres.fields import JSONField
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=1000)
    year = models.IntegerField()
    imdbid = models.CharField(max_length=1000)

    rated = models.CharField(max_length=1000, null=True, blank=True)
    released = models.CharField(max_length=1000, null=True, blank=True)
    runtime = models.CharField(max_length=1000, null=True, blank=True)
    genre = models.CharField(max_length=1000, null=True, blank=True)
    director = models.CharField(max_length=1000, null=True, blank=True)
    writer = models.CharField(max_length=1000, null=True, blank=True)
    actors = models.CharField(max_length=1000, null=True, blank=True)
    plot = models.CharField(max_length=1000, null=True, blank=True)
    language = models.CharField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=1000, null=True, blank=True)
    awards = models.CharField(max_length=1000, null=True, blank=True)
    poster = models.CharField(max_length=1000, null=True, blank=True)
    ratings = JSONField()
    metascore = models.CharField(max_length=1000, null=True, blank=True)
    imdbrating = models.CharField(max_length=1000, null=True, blank=True)
    imdbvotes = models.CharField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=1000, null=True, blank=True)
    dvd = models.CharField(max_length=1000, null=True, blank=True)
    boxoffice = models.CharField(max_length=1000, null=True, blank=True)
    production = models.CharField(max_length=1000, null=True, blank=True)
    website = models.CharField(max_length=1000, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @classmethod
    def should_override(cls, title, year, imdbid, **kwargs):
        movies = Movie.objects.filter(title=title, year=year, imdbid=imdbid)
        return movies.exists(), movies.first()

    class Meta:
        unique_together = ('title', 'year', 'imdbid')
        indexes = [
            models.Index(fields=['title', 'year']),
            models.Index(fields=['year']),
        ]


class Comment(models.Model):
    body = models.TextField()

    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
