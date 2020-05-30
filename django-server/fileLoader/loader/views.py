
from django.shortcuts import render  
from django.http import HttpResponse  
from loader.functions.functions import handle_uploaded_file  
from .form import fileLoadingForm  

def upload(request): 
    ''' function where we can access file form data and redirect to downloa form url'''
    if request.method == 'POST':  
        load = fileLoadingForm(request.POST, request.FILES)  
        if load.is_valid():  
            handle_uploaded_file(request.FILES['file'])  
            return HttpResponse("File uploaded successfuly")  
    else:  
        load = fileLoadingForm()  
        return render(request,"index.html",{'form':load})  

import os
from django.conf import settings
from django.http import HttpResponse, Http404

def download(request,file):
    print(file)
    file_path = os.path.join("upload/", file)  
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404