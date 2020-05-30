from .pdf2Csv import convert
from django.conf import settings

FILE_PATH=getattr(settings, "FILES_PATH", None)

class result:
    file=""
    param=""
    year=0000
    value=0

def handle_uploaded_file(f,load):  
    uploadFile(f)
    
    res =result()
    res.file="/download/"+convert(FILE_PATH,f.name)
    print("pdf file load and conveted to csv : "+res.file)
    res.param=load.cleaned_data['queryVariable']
    res.year=load.cleaned_data['queryYear']
    res.value=123456789.00
    return res
 

def uploadFile(f):
    print("going to upload pdf file :"+FILE_PATH+f.name)
    with open(FILE_PATH+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)
