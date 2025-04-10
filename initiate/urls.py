from django.urls import path
from .views import initiate_view

urlpatterns = [
    path('', initiate_view, name='initiate'),
]
