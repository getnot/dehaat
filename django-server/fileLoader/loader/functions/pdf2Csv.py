import pandas
import tabula
import time
import sys
import os
from os import path
from django.conf import settings

outputPath = getattr(settings, "FILES_PATH", None)



def convert(inputfilepath,inputfilename):
    ''' function to convert pdf file to csv 
        input => full qualified file name
    '''
    print("going to convert pdf file to csv")
    fileInputPath =inputfilepath+"/"+inputfilename
    validateFile(fileInputPath)
    createFolder(outputPath)
    
    print("pdf file validation done")
    milliseconds = int(round(time.time() * 1000))

    fileTempPath=outputPath+"temp_"+str(milliseconds)+".csv"
   
    outputFile=inputfilename.split(".")[0]+"_"+str(milliseconds)+".csv"
    fileOutputPath=outputPath+outputFile

    tabula.convert_into(fileInputPath, fileTempPath ,stream=True)
    print("pdf file to csv done")
    output=pandas.read_csv(fileTempPath,header=None)
    arr=output[[2][0]].str.split(" ",n=1,expand=True)
    output[[2][0]]=arr[0]
    output[[3][0]]=arr[1]
    output.to_csv(fileOutputPath,index=False, header=False)
    print("csv data is cleaned")
    return outputFile

def validateFile(file):
    ''' function to validate input file details 
        [path,extension]
    '''
    print("validation started")
    if(path.exists(file) == False):
        raise fileNotFound
 
    if(file[-3:]!= "pdf"):
        raise incorrectFileExtension

def createFolder(path):
    '''fucntion to create output path'''
    print("folder created:"+path)
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


if __name__ == "__main__":
    file=convert(sys.argv[1])
    print(outputPath+"/"+file)