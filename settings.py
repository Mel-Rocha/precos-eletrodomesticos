import os

from dotenv import load_dotenv
from tortoise import expand_db_url

load_dotenv()

db_url = os.getenv("DATABASE_URL")

TORTOISE_ORM = {
    "connections": {
        "default": expand_db_url(db_url),
    },
    "apps": {
        "models": {
            "models": ["apps.WishList.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}