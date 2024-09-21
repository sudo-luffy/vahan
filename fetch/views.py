from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .forms import CSVUploadForm
from core.tasks import process_csv_task

def csv_upload_view(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            csv_file = request.FILES['csv_file']
            
            # Save the uploaded file
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            uploaded_file_url = fs.url(filename)
            
            # Trigger the Celery task
            process_csv_task.delay(filename, email)
            
            return HttpResponse(f'File uploaded successfully, processing will be sent to {email}')
    else:
        form = CSVUploadForm()
    
    return render(request, 'fetch/upload.html', {'form': form})
