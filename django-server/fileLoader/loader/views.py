
from django.shortcuts import render  
from django.http import HttpResponse  
from .form import fileLoadingForm  
from django.conf import settings
import os
from django.conf import settings
import logging 
from django.http import HttpResponse, Http404
from loader.functions.functions import handle_uploaded_file  
from loader.functions.functions import fetchData 
from loader.functions.functions import fetchAllData 
from loader.functions.functions import clearFinancialData
from loader.functions.pdf2Csv import incorrectFileExtension
from loader.functions.pdf2Csv import incorrectPdfFile


logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 


def upload(request): 
    ''' function where we can access file form data and redirect to downloa form url'''
    if request.method == 'POST': 
        try:
            load = fileLoadingForm(request.POST, request.FILES)  
            if load.is_valid():  
                result=handle_uploaded_file(request.FILES['file'],load)
                return render(request, 'result.html', {'param':result.param,'year':result.year,'value':result.value,'file':result.file})
        except incorrectFileExtension as e:
            return render(request,"index.html",{'form':fileLoadingForm(),'error':'Incorrect file extension .. please load pdf only.'})
        except incorrectPdfFile as e:
            return render(request,"index.html",{'form':fileLoadingForm(),'error':'Please provide balance sheet as pdf'})
        except Exception as e:
            logging.debug(str(e)) 
            return render(request,"index.html",{'form':fileLoadingForm(),'error':'some error occured. pleasse try again...'}) 
    else:  
        load = fileLoadingForm()  
        return render(request,"index.html",{'form':load})  



def download(request,file):
    ''' function used to download file . file name will come as path variable'''
    file_path = os.path.join(getattr(settings, "FILES_PATH", None), file)  
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
    
def financialData(request):
    ''' financial data get and delete endpoint'''
    if request.method == 'GET': 
        param=request.GET.get('param', '')
        year=request.GET.get('year', 0)
        fileName=request.GET.get('fileName', '')
        if(param=='' and year==0 and fileName==''):
            return HttpResponse(fetchAllData())
        else:
            return HttpResponse(fetchData(fileName,param,year))
    elif request.method == 'DELETE': 
        clearFinancialData()
        return HttpResponse("deleted")
    else:
        raise Http404