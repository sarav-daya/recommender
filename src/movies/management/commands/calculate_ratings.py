from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model

from movies.models import Movie
from cfehome import utils as cfehome_utils

from movies.tasks import task_calculate_movie_ratings


User = get_user_model()  # for custom auth


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("count", nargs="?", default=1000, type=int)
        parser.add_argument("--all", action="store_true", default=False)

    def handle(self, *args, **options):
        count = options.get("count")
        all = options.get("all")
        task_calculate_movie_ratings(all=all, count=count)
