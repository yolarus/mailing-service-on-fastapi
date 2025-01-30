from os import getenv

from celery import Celery
from dotenv import load_dotenv

load_dotenv(".env")

celery_app = Celery("main",
                    broker=getenv("CELERY_BROKER_URL"),
                    backend=getenv("CELERY_RESULT_BACKEND"),
                    include=["celery_queue.tasks"])
