from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paosystem.settings")

app = Celery("paosystem")
app.config_from_object("django.conf:settings", namespace = "CELERY")
app.autodiscover_tasks()