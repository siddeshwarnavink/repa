import os

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from .forms import ProcessForm, ProcessFileForm
from .models import Process, ProcessFile
from .tasks import process_files_task

def initiate_view(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            process = form.save(commit=False)
            process.status = Process.ProcessStatus.FILE_UPLOADING
            process.preferred_education = ','.join(form.cleaned_data['preferred_education'])
            process.save()
            return redirect(reverse('fileupload', args=[process.id]))
        else:
            return render(request, 'initiate/initiate.html', {'form': form})
    else:
        form = ProcessForm()
        return render(request, 'initiate/initiate.html', {'form': form})

def fileupload_view(request, initiateId):
    process = get_object_or_404(Process, id=initiateId, status=Process.ProcessStatus.FILE_UPLOADING)
    #  Upload file
    if request.method == 'POST' and 'upload_file' in request.POST:
        form = ProcessFileForm(request.POST, request.FILES)
        if form.is_valid():
            process_file = form.save(commit=False)
            process_file.process = process
            process_file.status = ProcessFile.ProcessFileStatus.FILE_UPLOADED
            process_file.save()
            return redirect('fileupload', initiateId=initiateId)
    # Delete file
    if request.method == 'POST' and 'delete_file' in request.POST:
        file_id = request.POST.get('file_id')
        process_file = get_object_or_404(ProcessFile, id=file_id, process=process)
        if process_file.file:
            file_path = os.path.join(settings.MEDIA_ROOT, process_file.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)
        process_file.delete()
        return redirect('fileupload', initiateId=initiateId)
    # Render view
    else:
        form = ProcessFileForm()
        process_files = process.files.all()
        return render(request, 'initiate/fileupload.html', {
            'process': process,
            'form': form,
            'process_files': process_files,
        })

def fileupload_complete_view(request, initiateId):
    process_files_task.delay(initiateId)
    return redirect('queue-item', initiateId=initiateId)
