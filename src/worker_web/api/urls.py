from django.urls import path
from .views import it_works, worker_submit_code, worker_config_timeout

urlpatterns = [
    path('it_works/', it_works),
    path('worker_submit_code/', worker_submit_code),
    path('worker_config/timeout', worker_config_timeout)
]
