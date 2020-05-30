
from django.shortcuts import render  
from django.http import HttpResponse  
from loader.functions.functions import handle_uploaded_file  
from .form import fileLoadingForm  
from django.conf import settings

def upload(request): 
    ''' function where we can access file form data and redirect to downloa form url'''
    if request.method == 'POST': 
        try:
            load = fileLoadingForm(request.POST, request.FILES)  
            if load.is_valid():  
                result=handle_uploaded_file(request.FILES['file'],load)
                return render(request, 'result.html', {'param':result.param,'year':result.year,'value':result.value,'file':result.file})
        except Exception as e:
            print(e)
            load = fileLoadingForm()  
            return render(request,"index.html",{'form':load,'error':'some error occured. pleasse try again...'}) 
    else:  
        load = fileLoadingForm()  
        return render(request,"index.html",{'form':load})  

import os
from django.conf import settings
from django.http import HttpResponse, Http404

def download(request,file):
    ''' function used to download file . file name will come as path variable'''
    file_path = os.path.join(getattr(settings, "FILES_PATH", None), file)  
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404