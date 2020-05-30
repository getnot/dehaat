
from django.shortcuts import render  
from django.http import HttpResponse  
from loader.functions.functions import handle_uploaded_file  
from .form import fileLoadingForm  

def index(request): 
    ''' function where we can access file form data and redirect to downloa form url'''
    if request.method == 'POST':  
        load = fileLoadingForm(request.POST, request.FILES)  
        if load.is_valid():  
            handle_uploaded_file(request.FILES['file'])  
            return HttpResponse("File uploaded successfuly")  
    else:  
        load = fileLoadingForm()  
        return render(request,"index.html",{'form':load})  