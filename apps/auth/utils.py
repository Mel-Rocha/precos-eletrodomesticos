<<<<<<< HEAD
import os
import json
import hashlib
from datetime import datetime


SECRET_KEY = os.getenv("SECRET_KEY")


def generate_auth_token():
    data = {
        "timestamp": str(datetime.now().timestamp()),
        "secret_key": SECRET_KEY
    }
=======
import os
import json
import hashlib
from datetime import datetime


SECRET_KEY = os.getenv("SECRET_KEY")


def generate_auth_token():
    data = {
        "timestamp": str(datetime.now().timestamp()),
        "secret_key": SECRET_KEY
    }
>>>>>>> b9c9b7ce59051f80f8dd40d88d8dc081e9a64c07
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()