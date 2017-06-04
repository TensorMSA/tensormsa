from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoyai.settings')

app = Celery('hoyai')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.autodiscover_tasks(packages= 'cluster.service', related_name='task')

CELERYD_HIJACK_ROOT_LOGGER = False
from celery import signals

@signals.setup_logging.connect
def setup_logging(**kwargs):
    """Setup logging."""
    pass


def custom_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join('/root/', name + '.log'), 'w')
    logger.addHandler(handler)
    return logger

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))