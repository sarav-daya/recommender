import csv
import datetime

from faker import Faker
from pprint import pprint
from django.conf import settings

MOVIE_METADATA_CSV = settings.DATA_DIR / "movies_metadata.csv"
DATA_DIR = settings.BASE_DIR / "data"


def validate_date_str(date_text):
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
    except:
        return None
    return date_text


def load_movie_data(limit=10):
    with open(MOVIE_METADATA_CSV, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        dataset = []
        for i, row in enumerate(reader):
            # pprint(row)
            _id = row.get("id")
            try:
                _id = int(id)
            except:
                _id = None

            data = {
                "id": _id,
                "title": row.get("title"),
                "overview": row.get("overview"),
                "release_date": validate_date_str(row.get("release_date")),
            }
            dataset.append(data)
            if i + 1 > limit:
                break
        return dataset


def get_fake_profiles(count=10):
    fake = Faker()
    user_data = []
    for _ in range(count):
        profile = fake.profile()

        data = {
            "username": profile.get("username"),
            "email": profile.get("mail"),
            "is_active": True,
        }
        if "name" in profile:
            fname, lname = profile.get("name").split(" ")[:2]
            data["first_name"] = fname
            data["last_name"] = lname
        user_data.append(data)
    return user_data
