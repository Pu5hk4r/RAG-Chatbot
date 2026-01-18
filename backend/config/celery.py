# config/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('rag_chatbot')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# Periodic tasks
app.conf.beat_schedule = {
    'cleanup-old-documents': {
        'task': 'apps.documents.tasks.cleanup_old_documents',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
}

app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')