from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model

from movies.models import Movie
from cfehome import utils as cfehome_utils

from ratings.tasks import generate_fake_reviews
from ratings.models import Rating

User = get_user_model()  # for custom auth


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("count", nargs="?", default=10, type=int)
        parser.add_argument("--users", default=1000, type=int)
        parser.add_argument("--show-total", action="store_true", default=False)

    def handle(self, *args, **options):
        count = options.get("count")
        show_total = options.get("show_total")
        users_count = options.get("users")

        new_ratings = generate_fake_reviews(count=count, users=users_count)
        print(f"New ratings: {len(new_ratings)}")
        if show_total:
            qs = Rating.objects.count()
            print(f"Total ratings: {qs}")
