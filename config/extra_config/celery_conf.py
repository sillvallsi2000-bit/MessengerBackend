CELERY_BROKER_URL = "redis://redis:6379/1"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "redis://redis:6379/1"
CELERY_TIMEZONE = "UTC"

CELERY_BROKER_TRANSPORT_OPTIONS = {
    "visibility_timeout": 3600,
    "max_retries": 3,
}


CELERY_BEAT_SCHEDULE = {
    "say_hello": {"task": "apps.user.tasks.db_change", "schedule": 30},
}
