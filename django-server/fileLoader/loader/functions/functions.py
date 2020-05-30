from .pdf2Csv import convert
from django.conf import settings
from loader.models import financial_data
import pandas
import itertools
import logging 

logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

FILE_PATH=getattr(settings, "FILES_PATH", None)

class result:
    file=""
    param=""
    year=0000
    value=0

def handle_uploaded_file(f,load):
    ''' upload,convert and get data'''
    logger.debug("going to process file");
    res =result()
  
    uploadFile(f)
    outputFile=convert(FILE_PATH,f.name)
    loadDataInDb(outputFile)
    fetchData(res,load.cleaned_data['queryVariable'],load.cleaned_data['queryYear'])
    
    res.file="/download/"+outputFile
    return res
 

def uploadFile(f):
    ''' upload data'''
    logger.debug("going to upload pdf file");
    with open(FILE_PATH+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)
            
            
def loadDataInDb(file):
    '''load data  in db'''
    logger.debug("going to load csv  file in db");
    output=pandas.read_csv(FILE_PATH+file,header=None)
   
    year1=0000
    year2=0000
    for (param,value1,value2) in zip(output[0],output[1],output[2]):
        if(param == 'Particulars'):
           year1= value1
           year2= value2
        if(str(param) != 'nan' and param != 'Particulars'):
           fd1 = financial_data(field_name=param, field_value=value1 ,  year=year1)
           fd2 = financial_data(field_name=param, field_value=value2 ,  year=year2)
           fd1.save()
           fd1.save()
    
    for (param,value1,value2) in zip(output[3],output[5],output[6]):
        if(param == 'Particulars'):
           year1= value1
           year2= value2
        if(str(param) != 'nan' and param != 'Particulars'):
           fd1 = financial_data(field_name=param, field_value=value1 ,  year=year1)
           fd2 = financial_data(field_name=param, field_value=value2 ,  year=year2)
           fd1.save()
           fd1.save()

def fetchData(res,param,year):
    ''' fetch data from db'''
    logger.debug("fetching data from db");
    res.param=param
    res.year=year
    try:
        find_list = financial_data.objects.get(year=year)
        print(find_list)
        for data in find_list:
            print(p)
            res.value=data.field_value
    except Exception as e:
        logger.debug("exception while fetching data from db" + str(e));
    