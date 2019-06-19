from django.urls import path
from .views import *


urlpatterns = [
    path('it_works/', it_works),

    path('worker_submit_code/', worker_submit_code),

    path('worker_config/timeout', worker_config_timeout),
    path('worker_config/cpu_share', worker_config_cpu_share),
    path('worker_config/memory_limit', worker_config_memory_limit),
    path('worker_config/set_config', worker_config_set_config),

    path('celery/get_workers', celery_get_workers),
    path('celery/registered_tasks', celery_registered_tasks),
    path('celery/active_tasks', celery_active_tasks),
    path('celery/scheduled_tasks', celery_scheduled_tasks),
    path('celery/active_queues', celery_active_queues),
    path('celery/reserved_tasks', celery_reserved_tasks),
    path('celery/revoked_tasks', celery_revoked_tasks),
    path('celery/control_broadcast', celery_control_broadcast)
]

