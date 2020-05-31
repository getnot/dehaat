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
#    clearFinancialData()
    res =result()
  
    uploadFile(f)
    outputFile=convert(FILE_PATH,f.name)
    loadDataInDb(outputFile)
    
    res.file="/download/"+outputFile
    res.param=load.cleaned_data['queryVariable']
    res.year=load.cleaned_data['queryYear']
    res.value=fetchData(outputFile,res.param,res.year)
    
    return res
 

def uploadFile(f):
    ''' upload data'''
    logger.debug("going to upload pdf file");
    with open(FILE_PATH+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)
            
            
def loadDataInDb(fileName):
    '''load data  in db'''
    logger.debug("going to load csv  file in db");
    output=pandas.read_csv(FILE_PATH+fileName,header=None)
   
    year1=0000
    year2=0000
    for (param,value1,value2) in zip(output[0],output[1],output[2]):
        if(param == 'Particulars'):
           year1= value1
           year2= value2
        if(str(param) != 'nan' and param != 'Particulars'):
           fd1 = financial_data(field_name=param, field_value=value1 ,  year=year1 , file=fileName)
           fd2 = financial_data(field_name=param, field_value=value2 ,  year=year2 , file=fileName)
           fd1.save()
           fd2.save()
    
    for (param,value1,value2) in zip(output[3],output[5],output[6]):
        if(param == 'Particulars'):
           year1= value1
           year2= value2
        if(str(param) != 'nan' and param != 'Particulars'):
           fd1 = financial_data(field_name=param, field_value=value1 ,  year=year1 , file=fileName)
           fd2 = financial_data(field_name=param, field_value=value2 ,  year=year2 , file=fileName)
           fd1.save()
           fd2.save()

def fetchData(fileName,param,yearGiven):
    ''' fetch data from db'''
    logger.debug("fetching data from db");

    try:
#        print(financial_data.objects.all()) 
#        res.value= financial_data.objects.get(field_name=param,year=year,file=file).field_value
        print(" params : " + param);
        print(" year : " + str(yearGiven));
        print(" file : " + fileName);
       
        if(fileName == ''):
            find_list = financial_data.objects.filter(field_name=param,year=yearGiven)
        else:
            find_list = financial_data.objects.filter(field_name=param,year=yearGiven,file=fileName)
        
        for data in find_list:
            return data.field_value
    except Exception as e:
        print(e)
        logger.debug("exception while fetching data from db" + str(e));
    return 0
    
def fetchAllData():
    ''' fetch all data from db'''
    return financial_data.objects.all()

    
def clearFinancialData():
    dataList=financial_data.objects.all()
    for data in dataList:
        data.delete()
