from django.urls import path
from .views import it_works, worker_submit_code

urlpatterns = [
    path('it_works/', it_works),
    path('worker_submit_code/', worker_submit_code),
]
