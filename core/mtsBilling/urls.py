from django.urls import path
from .views import process_cdr_file

urlpatterns = [
    path('process-cdr-file/', process_cdr_file, name='process-cdr-file'),
]
