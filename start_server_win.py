import sys
import os
import pprint
import uvicorn
from app import main

this_dir = os.path.dirname(__file__)
app_dir = os.path.join(this_dir, "backend/app")
if app_dir not in sys.path:
    sys.path.append(app_dir)

env_file = os.path.abspath(".env")
if env_file:
    with open(env_file, "r") as file_:

        for line_ in file_.read().split("\n"):
            if line_ and not line_.startswith("#"):
                name, value = line_.split("=")
                os.environ[name] = value

os.system("python ./backend/app/app/backend_pre_start.py")
os.system("python ./backend/app/app/initial_data.py")

PORT = os.environ.get("PORT", 5678)
HOST = os.environ.get("HOST", "127.0.0.1")

uvicorn.run(main.app, host=HOST, port=PORT)