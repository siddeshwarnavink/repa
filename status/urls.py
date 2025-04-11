from django.urls import path
from .views import queue_view, queue_item_view

urlpatterns = [
    path('queue/', queue_view, name='queue'),
    path('queue/<int:initiateId>', queue_item_view, name='queue-item'),
]
