from django.urls import path
from .views import it_works

urlpatterns = [
    path('it_works/', it_works)
]
