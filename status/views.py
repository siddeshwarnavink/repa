from django.shortcuts import render, get_object_or_404
from initiate.models import Process

def queue_view(request):
    processes = Process.objects.exclude(status=Process.ProcessStatus.FILE_UPLOADING)
    return render(request, 'status/queue.html', {'processes': processes})

def queue_item_view(request, initiateId):
    process = get_object_or_404(Process, id=initiateId)
    process_files = process.files.all()
    return render(request, 'status/queue-item.html', {
        'process': process,
        'process_files': process_files
    })
