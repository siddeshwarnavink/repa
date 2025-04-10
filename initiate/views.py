from django.shortcuts import render, redirect
from .forms import ProcessForm
from .models import Process

def initiate_view(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            process = form.save(commit=False)
            process.status = Process.ProcessStatus.FILE_UPLOADING
            process.preferred_education = ','.join(form.cleaned_data['preferred_education'])
            process.save()
            return redirect('fileupload')
        else:
            return render(request, 'initiate/initiate.html', {'form': form})
    else:
        form = ProcessForm()
        return render(request, 'initiate/initiate.html', {'form': form})

def fileupload_view(request):
    return render(request, 'initiate/fileupload.html')
