import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DCA.settings")
app = Celery("DCA")

app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

# Add the following line to enable broker connection retries on startup
app.conf.broker_connection_retry_on_startup = True

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')