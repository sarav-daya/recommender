import random

from movies.models import Movie
from django.contrib.auth import get_user_model
from .models import Rating, RatingChoice

User = get_user_model()


def generate_fake_reviews(count=100, users=10, null_avg=False):
    user_s = User.objects.first()  # get the first id
    user_e = User.objects.last()  # get the last id
    print(user_s.id)
    print(user_e.id)
    # generate a list of user ids
    random_user_ids = random.sample(range(user_s.id, user_e.id), users)
    users = User.objects.filter(id__in=random_user_ids)

    # get a list of movies and order by random "?" signifies order by randdom
    if null_avg:
        movies = Movie.objects.filter(rating_avg__isnull=True).order_by("?")[:count]
    else:
        movies = Movie.objects.all().order_by("?")[:count]

    n_ratings = movies.count()
    rating_choices = [x for x in RatingChoice.values if x is not None]
    user_ratings = [random.choice(rating_choices) for _ in range(0, n_ratings)]

    new_ratings = []
    for movie in movies:
        rating_obj = Rating.objects.create(
            content_object=movie,
            value=user_ratings.pop(),
            user=random.choice(users),
        )
        new_ratings.append(rating_obj.id)
    return new_ratings
