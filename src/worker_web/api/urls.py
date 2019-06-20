from django.urls import re_path
from .views import *


urlpatterns = [
    # re_path('it_works/', it_works),

    re_path(r'^worker_submit_code\/?$', worker_submit_code),

    re_path(r'^worker_config/timeout\/?$', worker_config_timeout),
    re_path(r'^worker_config/cpu_share\/?$', worker_config_cpu_share),
    re_path(r'^worker_config/memory_limit\/?$', worker_config_memory_limit),
    re_path(r'^worker_config/set_config\/?$', worker_config_set_config),

    re_path(r'^celery/get_workers\/?$', celery_get_workers),
    re_path(r'^celery/registered_tasks\/?$', celery_registered_tasks),
    re_path(r'^celery/active_tasks\/?$', celery_active_tasks),
    re_path(r'^celery/scheduled_tasks\/?$', celery_scheduled_tasks),
    re_path(r'^celery/active_queues\/?$', celery_active_queues),
    re_path(r'^celery/reserved_tasks\/?$', celery_reserved_tasks),
    re_path(r'^celery/revoked_tasks\/?$', celery_revoked_tasks),
    re_path(r'^celery/control_broadcast\/?$', celery_control_broadcast)
]

