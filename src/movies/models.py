from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.query import QuerySet
from ratings.models import Rating
from django.utils import timezone
from django.db.models import Q
import datetime

RATING_CALC_TIME_IN_DAYS = 3


class MovieQuerySet(models.QuerySet):
    def needs_updating(self):
        now = timezone.now()
        days_ago = now - timezone.timedelta(days=RATING_CALC_TIME_IN_DAYS)
        return self.filter(
            Q(rating_last_updated__isnull=True) | Q(rating_last_updated__lte=days_ago)
        )


class MovieManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return MovieQuerySet(self.model, using=self._db)

    def needs_updating(self):
        return self.get_queryset().needs_updating()


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=120, unique=True)
    overview = models.TextField()
    release_date = models.DateField(
        blank=True, null=True, auto_now=False, auto_now_add=False
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = GenericRelation(Rating)
    rating_count = models.IntegerField(blank=True, null=True)
    rating_avg = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True
    )
    rating_last_updated = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )

    objects = MovieManager()

    def __str__(self):
        if not self.release_date:
            return f"{self.title}"
        return f"{self.title} ({self.release_date.year})"

    def rating_avg_display(self):
        now = timezone.now()

        if not self.rating_last_updated:
            return self.calculate_rating()

        if self.rating_last_updated > now - datetime.timedelta(
            days=RATING_CALC_TIME_IN_DAYS
        ):
            return self.rating_avg

        return self.calculate_rating()

    def calculate_ratings_count(self):
        return self.ratings.all().count()

    def calculate_ratings_avg(self):
        return self.ratings.avg()

    def calculate_rating(self, save=True):
        rating_avg = self.calculate_ratings_avg()
        rating_count = self.calculate_ratings_count()

        self.rating_avg = rating_avg
        self.rating_count = rating_count

        self.rating_last_updated = timezone.now()

        if save:
            self.save()
        return rating_avg
