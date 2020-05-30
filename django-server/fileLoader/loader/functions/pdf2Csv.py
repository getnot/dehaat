import pandas
import tabula
import time
import sys
import os
from os import path
from django.conf import settings
import logging 


logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

outputPath = getattr(settings, "FILES_PATH", None)



def convert(inputfilepath,inputfilename):
    ''' function to convert pdf file to csv 
        input => full qualified file name
    '''
    logger.debug("going to convert pdf file to csv")
    fileInputPath =inputfilepath+"/"+inputfilename
    validateFile(fileInputPath)
    createFolder(outputPath)
    
    logger.debug("pdf file validation done")
    milliseconds = int(round(time.time() * 1000))

    fileTempPath=outputPath+"temp_"+str(milliseconds)+".csv"
   
    outputFile=inputfilename.split(".")[0]+"_"+str(milliseconds)+".csv"
    fileOutputPath=outputPath+outputFile

    tabula.convert_into(fileInputPath, fileTempPath ,stream=True)
    logger.debug("pdf file to csv done")
    
    try:
        output=pandas.read_csv(fileTempPath,header=None)
        arr=output[[2][0]].str.split(" ",n=1,expand=True)
        output[[2][0]]=arr[0]
        output[[3][0]]=arr[1]
        output.to_csv(fileOutputPath,index=False, header=False)
        logger.debug("csv data is cleaned")
    except Exception as e:
        logger.debug("error while data cleaning"+str(e))
        raise incorrectPdfFile
        
    return outputFile

def validateFile(file):
    ''' function to validate input file details 
        [path,extension]
    '''
    logger.debug("validation started")
    if(path.exists(file) == False):
        raise fileNotFound
 
    if(file[-3:]!= "pdf"):
        raise incorrectFileExtension

def createFolder(path):
    '''fucntion to create output path'''
    logger.debug("folder created:"+path)
    if not os.path.exists(path):
        os.makedirs(path)


class Error(Exception):
    """Base class for other exceptions"""
    pass
class fileNotFound(Error):
    """Raised when file not found"""
    pass
class incorrectFileExtension(Error):
    """Raised when File with incorrect extension if provided in input"""
    pass
class incorrectPdfFile(Error):
    """Rasie when other pdf file is given as input instead of balance sheet"""
    pass


if __name__ == "__main__":
    file=convert(sys.argv[1])
    print(outputPath+"/"+file)