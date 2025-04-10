from django.urls import path
from .views import initiate_view, fileupload_view

urlpatterns = [
    path('', initiate_view, name='initiate'),
    path('upload', fileupload_view, name='fileupload'),
]
