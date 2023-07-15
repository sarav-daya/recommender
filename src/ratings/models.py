from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Avg
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.

User = settings.AUTH_USER_MODEL  # auth.User


class RatingChoice(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    __empty__ = "Rate this"


class RatingQuerySet(models.QuerySet):
    def avg(self):
        return self.aggregate(average=Avg("value"))["average"]


class RatingManager(models.Manager):
    def get_queryset(self):
        return RatingQuerySet(self.model, self._db)

    def avg(self):
        return self.get_queryset().avg()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(null=True, blank=True, choices=RatingChoice.choices)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    active = models.BooleanField(default=True)
    active_update_timestamps = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )
    timestamps = models.DateTimeField(auto_now_add=True)

    objects = RatingManager()

    class Meta:
        ordering = ["-timestamps"]


def rating_post_save(sender, instance, created, *args, **kwargs):
    if created:
        _id = instance.id
        if instance.active:
            qs = Rating.objects.filter(
                content_type=instance.content_type,
                object_id=instance.object_id,
                user=instance.user,
            ).exclude(id=_id, active=True)

            if qs.exists():
                qs = qs.exclude(active_update_timestamps__isnull=False)
                qs.update(active=False, active_update_timestamps=timezone.now())


post_save.connect(rating_post_save, sender=Rating)
