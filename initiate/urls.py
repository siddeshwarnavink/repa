from django.urls import path
from .views import initiate_view, fileupload_view, fileupload_complete_view

urlpatterns = [
    path('', initiate_view, name='initiate'),
    path('upload/<int:initiateId>', fileupload_view, name='fileupload'),
    path('upload/<int:initiateId>/complate', fileupload_complete_view, name='fileupload-complate')
]
