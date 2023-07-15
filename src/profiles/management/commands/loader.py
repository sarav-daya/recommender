from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model

from movies.models import Movie
from cfehome import utils as cfehome_utils

User = get_user_model()  # for custom auth


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("count", nargs="?", default=10, type=int)
        parser.add_argument("--show-total", action="store_true", default=False)
        parser.add_argument("--movies", action="store_true", default=False)
        parser.add_argument("--users", action="store_true", default=False)

    def handle(self, *args, **options):
        count = options.get("count")
        show_total = options.get("show_total")
        load_movies = options.get("movies")
        generate_users = options.get("users")

        if generate_users:
            profiles = cfehome_utils.get_fake_profiles(count)
            new_users = []

            for profile in profiles:
                new_users.append(User(**profile))

            user_bulk = User.objects.bulk_create(
                new_users,
                ignore_conflicts=True,
                batch_size=10_000,
            )
            print(f"New users created {len(user_bulk)} users")

            if show_total:
                print(f"Total users: {User.objects.count()}")

        if load_movies:
            movies_dataset = cfehome_utils.load_movie_data(limit=count)
            movies_new = [Movie(**movie) for movie in movies_dataset]
            movies_bulk = Movie.objects.bulk_create(movies_new, ignore_conflicts=True)
            print(f"New Movies: {len(movies_bulk)}")

            if show_total:
                print(f"Total movies in the database : {Movie.objects.count()}")
